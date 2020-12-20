import tkinter as tk
from networkx_viewer.graph_canvas import GraphCanvas
from networkx_viewer.tokens import (NodeToken, EdgeToken, TkPassthroughNodeToken,
                    TkPassthroughEdgeToken)
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

        self.canvas = GraphCanvas(graph, width=600, height=400, **kwargs)
        self.canvas.grid(row=0, column=0, rowspan=bottom_row+2, sticky='NESW')
        self.canvas.onNodeSelected = self.onNodeSelected
        self.canvas.onEdgeSelected = self.onEdgeSelected

        r = 0   # Current row
        assert r == bottom_row, "Set bottom_row to %d" % r
        
    def onNodeSelected(self, node_name, node_dict):
        self.tbl_attr.build(node_dict)
        self.lbl_attr.config(text="Attributes of node '%s'"%node_name)

    def onEdgeSelected(self, edge_name, edge_dict):
        self.tbl_attr.build(edge_dict)
        self.lbl_attr.config(text="Attributes of edge between '%s' and '%s'"%
                                    edge_name[:2])
        
        
class TkPassthroughViewerApp(ViewerApp):
    def __init__(self, graph, **kwargs):
        ViewerApp.__init__(self, graph,
            NodeTokenClass=TkPassthroughNodeToken,
            EdgeTokenClass=TkPassthroughEdgeToken, **kwargs)