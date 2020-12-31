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
reader = csv.DictReader(open('/home/user/list4'), fieldnames=['qube','netvm','color','klass'],delimiter='|')

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


Viewer = TkPassthroughViewerApp
app = Viewer(G)
app.mainloop()

