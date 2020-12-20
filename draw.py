#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 10:35:19 2020

@author: user
"""

# libraries
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
 
qubes = ['A', 'B', 'C','E','F','G','H']
netvms = ['C', 'D', 'D','D','E','H','I']
df = pd.DataFrame({ 'from':qubes, 'to':netvms})
df
 
# Build the graph
G=nx.from_pandas_edgelist(df, 'from', 'to')
 
# Plot it
nx.draw(G, with_labels=True)
plt.show()
