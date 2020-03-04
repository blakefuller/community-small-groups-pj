import sys
import igraph

#read from file and store names as a list of lists
fp = open("group1.txt", "r")
lines = fp.readlines()
names = []
for line in lines:
    names.append(line.rstrip("\n").split(","))

print(names)