import networkx as nx
import tkinter as tk
import subprocess
from tkinter import scrolledtext
from networkx_viewer.graph_canvas import GraphCanvas
from networkx_viewer.tokens import (NodeToken, EdgeToken)


def qstart(qube):
    lcommand = ['/usr/bin/qvm-start', qube]
    subprocess.call(lcommand)


def qshutdown(qube):
    lcommand = ['/usr/bin/qvm-shutdown', qube]
    subprocess.call(lcommand)


def qname(self, event):
    from tkinter import simpledialog
    newname = simpledialog.askstring("Change Display name",
                                     "What is the new name?")
    item = self._get_id(event)
    # name = self.dispG.nodes[item]['dataG_id']
    token = self.dispG.nodes(data=True)[item]['token']
    token.itemconfig(token.label, text=newname)
    bbox = token.bbox(token.label)
    bbox = [abs(x) for x in bbox]
    br = (max((bbox[0] + bbox[2]), 40), max((bbox[1]+bbox[3]), 20))
    token.config(width=br[0], height=br[1]+7)
    # Place label and marker
    mid = (int(br[0]/2.0), int(br[1]/2.0)+7)
    token.coords(token.label, mid)
    token.coords(token.marker, mid[0]-5, 0, mid[0]+5, 10)


def qfirewall(qube):
    lcommand = ['qubes-vm-settings --tab firewall', qube]
    subprocess.call(lcommand)


class CustomGraphCanvas(GraphCanvas):
    def __init__(self, graph, **kwargs):
        self.dataG = graph

        self.dispG = nx.MultiGraph()

        self._drag_data = {'x': 0, 'y': 0, 'item': None}
        self._pan_data = (None, None)
        self._node_filters = ["str(u)!='-'","str(u)!='dom0'"]

        # Undo list
        self._undo_states = []
        self._redo_states = []
        self._undo_suspend = False

        # Create a display version of this graph
        # If requested, plot only within a certain level of the home node
        home_node = kwargs.pop('home_node', None)
        if home_node:
            levels = kwargs.pop('levels', 1)
            graph = self._neighbors(home_node, levels=levels, graph=graph)

        # Class to use when create a node widget
        self._NodeTokenClass = kwargs.pop('NodeTokenClass',
                                          NodeToken)
        assert issubclass(self._NodeTokenClass, NodeToken), \
            "NodeTokenClass must be inherited from NodeToken"
        self._EdgeTokenClass = kwargs.pop('EdgeTokenClass',
                                          EdgeToken)
        assert issubclass(self._EdgeTokenClass, EdgeToken), \
            "NodeTokenClass must be inherited from NodeToken"

        ###
        # Now we can do UI things
        ###
        tk.Canvas.__init__(self, **kwargs)

        self._plot_graph(graph)

        self.center_on_node(home_node or next(iter(graph.nodes())))

        self.tag_bind('node', '<ButtonPress-1>', self.onNodeButtonPress)
        self.tag_bind('node', '<ButtonRelease-1>', self.onNodeButtonRelease)
        self.tag_bind('node', '<B1-Motion>', self.onNodeMotion)

#        self.tag_bind('edge', '<Button-1>', self.onEdgeClick)
        self.tag_bind('edge', '<Button-3>', self.onEdgeRightClick)

        self.bind('<ButtonPress-1>', self.onPanStart)
        self.bind('<ButtonRelease-1>', self.onPanEnd)
        self.bind('<B1-Motion>', self.onPanMotion)


    class CustomNoteToken(NodeToken):

        def __init__(self, host_canvas, data, node_name):
            tk.Canvas.__init__(self, width=50, height=70)

            self._host_canvas = host_canvas
            self._complete = True
            self._marked = False
            self._default_bg = 'Red'

            self.bind('<ButtonPress-1>', self._host_event('onNodeButtonPress'))
            self.bind('<ButtonRelease-1>', self._host_event('onNodeButtonRelease'))
            self.bind('<B1-Motion>', self._host_event('onNodeMotion'))

            self.render(data, node_name)

        def render(self, data, node_name):
            self.config(width=280, height=200)
            w = tk.Frame(self, bg='blue', bd=3, width=280, height=200)
            w.pack()
            text = tk.scrolledtext.ScrolledText(w,
                                                wrap=tk.WORD,
                                                width=30,
                                                height=10,
                                                bg='white'
                                                )
            text.pack(side='right', expand=False)

    def onTokenRightClick(self, event):
        item = self._get_id(event)
        name = self.dispG.nodes[item]['dataG_id']
        popup = tk.Menu(self, tearoff=0)
        popup.add_command(label='Start',
                          command=lambda: qstart(name))
        popup.add_command(label='Shutdown',
                          command=lambda: qshutdown(name))
        popup.add_command(label='Rename',
                          command=lambda: qname(self, event))
        popup.add_command(label='Mark', command=lambda: self.mark_node(item))
        popup.add_command(label='Hide', command=lambda: self.hide_node(item))
        popup.add_command(label='Note', command=lambda: self.add_note(event))
        try:
            popup.post(event.x_root, event.y_root)
        finally:
            popup.grab_release()

    def onEdgeRightClick(self, event):
        item = self._get_id(event, 'edge')
        for u, v, k, d in self.dispG.edges(keys=True, data=True):
            if d['token'].id == item:
                source = d['dataG_id'][0]
                break

        popup = tk.Menu(self, tearoff=0)
        popup.add_command(label='Mark', command=lambda: self.mark_edge(u, v, k))
        popup.add_command(label='Firewall', command=lambda: qfirewall(source))
        d['token'].customize_menu(popup)

        try:
            popup.post(event.x_root, event.y_root)
        finally:
            popup.grab_release()

    def see_note(self, event):
        item = self._get_id(event)
        name = self.dispG.nodes[item]['dataG_id']
        if 'Details' in self.dataG.nodes[name]:
            Details = self.dataG.nodes[name]['Details']
            self.placeholder = self.create_text(5, 5, anchor='nw',
                                                fill="darkblue", text=name)
            for key, value in Details.items():
                self.insert(self.placeholder, tk.END, "\n"+key+":"+"\t"+value)

    def delete_note(self, event):
        self.delete(self.placeholder)

    def add_note(self, event):
        """Create a token for the data_node at the given coordinater"""
        item = self._get_id(event)
        source_name = self.dispG.nodes[item]['dataG_id']
        (x, y) = (event.x+100, event.y-100)
        data = self.dataG[source_name]
        data_node = source_name+"_note"
        # Apply filter to node to make sure we should draw it
        for filter_lambda in self._node_filters:
            try:
                draw_flag = eval(filter_lambda, {'u': data_node, 'd': data})
            except Exception as e:
                self._show_filter_error(filter_lambda, e)
                return
            # Filters are applied as an AND (ie, all must be true)
            # So if one is false, exit
            if draw_flag is False:
                return
        token = self.CustomNoteToken(self, data, data_node)
        id = self.create_window(x, y, window=token, anchor=tk.CENTER,
                                tags='node')
        self.dispG.add_node(id, dataG_id=data_node, token_id=id, token=token)
       #self.node_list.insert(tk.END, id)
        self.dataG.add_node(data_node)
        return id


class CustomNodeToken(NodeToken):
    def render(self, data, node_name):
        self.config(width=50, height=50)

        # Set color and other options
        marker_options = {'fill':       data.get('color', 'red'),
                          'outline':    'black'}
        self.marker = self.create_oval(0, 0, 10, 10, **marker_options)
        self.label = self.create_text(0, 0, text=node_name)
        cfg = self.itemconfig(self.label)
        for k, v in cfg.copy().items():
            cfg[k] = data.get('label_'+k, cfg[k][-1])
        self.itemconfig(self.label, **cfg)
        self._default_label_color = data.get('label_fill', 'black')
        # Figure out how big we really need to be
        bbox = self.bbox(self.label)
        bbox = [abs(x) for x in bbox]
        br = (max((bbox[0] + bbox[2]), 20), max((bbox[1]+bbox[3]), 20))

        self.config(width=br[0], height=br[1]+7)
        # Place label and marker
        mid = (int(br[0]/2.0), int(br[1]/2.0)+7)
        self.coords(self.label, mid)
        self.coords(self.marker, mid[0]-5, 0, mid[0]+5, 10)
        self.bind('<Enter>', self._host_event('see_note'))
        self.bind('<Leave>', self._host_event('delete_note'))
        if 'Details' in data:
            if data['Details']['klass'] == 'TemplateVM':
                self.mark()
            if data['Details']['klass'] == 'StandaloneVM':
                self.config(bg='blue')


class ViewerApp(tk.Tk):
    """Example simple GUI to plot a NetworkX Graph"""
    def __init__(self, graph, **kwargs):
        """Additional keyword arguments beyond graph are passed down to the
        GraphCanvas.  See it's docs for details"""
        tk.Tk.__init__(self)
        self.geometry('600x400')
        self.title('Qubes Network Viewer')

        bottom_row = 0
        self.columnconfigure(0, weight=1)
        self.rowconfigure(bottom_row, weight=1)

        self.canvas = CustomGraphCanvas(graph, NodeTokenClass=CustomNodeToken,
                                        width=400, height=300, **kwargs)
        self.canvas.grid(row=0, column=0, rowspan=bottom_row+2, sticky='NESW')
        self.canvas.onNodeSelected = self.onNodeSelected
#        self.canvas.onEdgeSelected = self.onEdgeSelected

        r = 0   # Current row
        assert r == bottom_row, "Set bottom_row to %d" % r

    def onNodeSelected(self, node_name, node_dict):
        return


class TkPassthroughViewerApp(ViewerApp):
    def __init__(self, graph, **kwargs):
        ViewerApp.__init__(self, graph, **kwargs)
