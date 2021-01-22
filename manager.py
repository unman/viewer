#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 10:35:19 2020

@author: user
    """

# libraries

import argparse
import pandas as pd
import networkx as nx
from viewer import TkPassthroughViewerApp

import csv
reader = csv.DictReader(open('/home/user/list11'), fieldnames=['qube', 'netvm',
                                'label', 'klass', 'template', 'IP', 'IPBACK',
                                'GATEWAY', 'visible_ip', 'visible_netmask',
                                'visible_gateway'], delimiter='|')
parser = argparse.ArgumentParser(description="Display information about qubes network")
parser.add_argument("--templates", help="Show template relationships",
                    action="store_true")
parser.add_argument("--all", help="Show network for all qubes including Templates",
                    action="store_true")
args = parser.parse_args()

d = {}
e = {}
for row in reader:
    key = row.pop('qube')
    d[key] = row

for key, value in d.items():
    if args.templates:
        if value['klass'] != 'TemplateVM':
            e[key] = value['template']
        else:
            e[key] = value['netvm']
    else:
        if args.all:
                e[key] = value['netvm']
        else:
            if value['netvm'] != '-':
                e[key] = value['netvm']

qubes = list(e.keys())
netvms = list(e.values())
df = pd.DataFrame({'from': qubes, 'to': netvms})
G = nx.from_pandas_edgelist(df, 'from', 'to')

for qube in G.nodes:
    if qube != '-':
        G.nodes[qube]['color'] = d[qube]['label']
        G.nodes[qube]['Details'] = d[qube]
        if (d[qube]['klass'] == 'TemplateVM') and (d[qube]['netvm'] != '-'):
            G.nodes[qube]['label_fill'] = 'red'
Viewer = TkPassthroughViewerApp
app = Viewer(G)
app.mainloop()
