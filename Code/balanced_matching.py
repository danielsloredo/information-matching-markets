import numpy as np
import numpy as np
import networkx as nx
import random as ra
import matplotlib.pyplot as plt
import math 

g = nx.Graph()

for i in range(10):
    g.add_node(i)

print(g.nodes())


for i in range(4):
    for j in range(5):
        g.add_edge(i,j+4)

print(g.edges())

print('testing github')

print('code succesfull')