#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 10:35:19 2020

@author: user
"""

# libraries

import pandas as pd
import networkx as nx
import tkinter as tk
from networkx_viewer import NodeToken, GraphCanvas
from viewer import TkPassthroughViewerApp, ViewerApp
Viewer = TkPassthroughViewerApp
#BasicViewer = ViewerApp
df = pd.read_csv('/home/user/list',sep='|',header=None, names={'col','col1'},keep_default_na=False)
G = nx.from_pandas_edgelist(df, source='col', target='col1')

app = Viewer(G)
app.mainloop()

