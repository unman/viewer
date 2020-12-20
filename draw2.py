#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 10:35:19 2020

@author: user
"""

# libraries
import subprocess
import sys
import pandas as pd
import networkx as nx
from networkx_viewer import Viewer


# Sample data - list3 is output from qvm-ls -O name,netvm --raw-data
d = {}
filelist = open('/home/user/list3','r').read().splitlines()
for line in filelist:
    (key, val) = line.split("|")
    d[(key)] = val
#   
qubes = list(d.keys())
netvms = list(d.values())
df = pd.DataFrame({ 'from':qubes, 'to':netvms})
G = nx.from_pandas_edgelist(df, 'from', 'to' )
app = Viewer(G)
app.mainloop()
