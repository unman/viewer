import tkinter as tk
import subprocess

from networkx_viewer.graph_canvas import GraphCanvas
from networkx_viewer.tokens import (NodeToken, EdgeToken)

def qstart(qube):
    lcommand = ['/usr/bin/qvm-start',qube]
    subprocess.call(lcommand) 

def qshutdown(qube):
    lcommand = ['/usr/bin/qvm-shutdown',qube]
    subprocess.call(lcommand) 
    
class CustomGraphCanvas(GraphCanvas):
    def onTokenRightClick(self, event):
        item = self._get_id(event)
        name = self.dispG.nodes[item]['dataG_id']
        popup = tk.Menu(self, tearoff=0)
        popup.add_command(label='Start', 
                          command=lambda: qstart(name))
        popup.add_command(label='Shutdown',
                          command=lambda: qshutdown(name))
        # popup.add_command(label='Hide', command=lambda: self.hide_node(item),
        #                      accelerator='H')
        try:
            popup.post(event.x_root, event.y_root)
        finally:
            popup.grab_release()
 
class CustomNodeToken(NodeToken):
    def render(self, data, node_name):
        self.config(width=50, height=50)
        
        # Set color and other options
        marker_options = {'fill':       data.get('color','red'),
                          'outline':    'black'}
        self.marker = self.create_oval(0,0,10,10, **marker_options)
        self.label = self.create_text(0, 0, text=node_name)
        cfg = self.itemconfig(self.label)
        for k,v in cfg.copy().items():
            cfg[k] = data.get('label_'+k, cfg[k][-1])
        self.itemconfig(self.label, **cfg)
        self._default_label_color = data.get('label_fill','black')
        # Figure out how big we really need to be
        bbox = self.bbox(self.label)
        bbox = [abs(x) for x in bbox]
        br = ( max((bbox[0] + bbox[2]),20), max((bbox[1]+bbox[3]),20) )

        self.config(width=br[0], height=br[1]+7)
        # Place label and marker
        mid = ( int(br[0]/2.0), int(br[1]/2.0)+7 )
        self.coords(self.label, mid)
        self.coords(self.marker, mid[0]-5,0, mid[0]+5,10)


        
class ViewerApp(tk.Tk):
    """Example simple GUI to plot a NetworkX Graph"""
    def __init__(self, graph, **kwargs):
        """Additional keyword arguments beyond graph are passed down to the
        GraphCanvas.  See it's docs for details"""
        tk.Tk.__init__(self)
        self.geometry('1000x600')
        self.title('Qubes Network Viewer')

        bottom_row = 0
        self.columnconfigure(0, weight=1)
        self.rowconfigure(bottom_row, weight=1)

        self.canvas = CustomGraphCanvas(graph, NodeTokenClass=CustomNodeToken, width=600, height=400,  **kwargs)
        self.canvas.grid(row=0, column=0, rowspan=bottom_row+2, sticky='NESW')
        self.canvas.onNodeSelected = self.onNodeSelected
#        self.canvas.onEdgeSelected = self.onEdgeSelected

        r = 0   # Current row
        assert r == bottom_row, "Set bottom_row to %d" % r
        
    def onNodeSelected(self, node_name, node_dict):
        return
#        self.tbl_attr.build(node_dict)
#        self.lbl_attr.config(text="Attributes of node '%s'"%node_name)

#    def onEdgeSelected(self, edge_name, edge_dict):
#        self.tbl_attr.build(edge_dict)
#        self.lbl_attr.config(text="Attributes of edge between '%s' and '%s'"%
#                                    edge_name[:2])
        
class TkPassthroughViewerApp(ViewerApp):
    def __init__(self, graph, **kwargs):
        ViewerApp.__init__(self, graph, **kwargs)
