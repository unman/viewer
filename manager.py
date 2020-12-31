#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 10:35:19 2020

@author: user
"""

# libraries

import pandas as pd
import networkx as nx
from viewer import TkPassthroughViewerApp
d = {}
filelist = open('/home/user/list4','r').read().splitlines()
for line in filelist:
    (key, val) = line.split("|")
    d[(key)] = val

qubes = list(d.keys())
netvms = list(d.values())
df = pd.DataFrame({ 'from':qubes, 'to':netvms})

df = pd.DataFrame({ 'from':qubes, 'to':netvms})
G = nx.from_pandas_edgelist(df, 'from', 'to' )

Viewer = TkPassthroughViewerApp

G.nodes['net-tablet']['color'] = 'grey'
G.nodes['tor']['color'] = 'blue'

app = Viewer(G)
app.mainloop()

