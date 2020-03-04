import sys
import igraph

fp = open("group1.txt", "r")
lines = fp.readlines()
names = []
for line in lines:
    names.append(line.rstrip("\n").split(","))

print(names)