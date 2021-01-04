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

import csv
reader = csv.DictReader(open('/home/user/list11'), fieldnames=['qube','netvm','label','klass','template','IP','IPBACK','GATEWAY','visible_ip','visible_netmask','visible_gateway'],delimiter='|')

d = {}
e = {}
for row in reader:
    key = row.pop('qube')
    d[key] = row
    
for key,value in d.items():
    if value['klass'] != 'TemplateVM':
        e[key] = value['netvm']
    else:
        if value['netvm'] != '-':
            e[key] = value['netvm']
    
qubes = list(e.keys())
netvms = list(e.values())
df = pd.DataFrame({ 'from':qubes, 'to':netvms})
G = nx.from_pandas_edgelist(df, 'from', 'to' )

for qube in G.nodes:
    if qube != '-':
        G.nodes[qube]['color'] = d[qube]['label']
        G.nodes[qube]['Details'] = d[qube]
        if d[qube]['klass'] == 'TemplateVM':
            G.nodes[qube]['label_fill'] = 'red'
        #if G.has_edge(qube,'-'):
         #   G.remove_edge(qube,'-')

#G.remove_edge('net-tablet','-')
Viewer = TkPassthroughViewerApp
app = Viewer(G)
app.mainloop()

