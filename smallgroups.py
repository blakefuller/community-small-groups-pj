import sys
from igraph import *

#read from file and store names as a list of lists
fp = open("group1.txt", "r")
lines = fp.readlines()
names = []
graphNames = []
for line in lines:
    names.append(line.rstrip("\n").split(","))
    graphNames.append(line.rstrip("\n"))


graph = Graph()
graph.add_vertices(graphNames)

graph.add_edge("Lyman Tucker", "Cassie Lambert")
print(graph)