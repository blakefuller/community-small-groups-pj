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

# graph.add_edge("Lyman Tucker", "Cassie Lambert")    
print(graph)

def getIteration(listOfPeople, homeConnectionGraph):

    # create list of iterations and list for storing groups of the current iteration
    notInGroup = listOfPeople
    currentIteration = []
    currentGroup = []

    while notInGroup:
        for person in listOfPeople:
            if len(currentGroup) == 4:
                currentIteration.append(currentGroup)
                currentGroup.clear()

            # current group to put people into (person in spot 1 should be host)
            if person in notInGroup:
                if not currentGroup:
                    currentGroup.append(person)
                    notInGroup.remove(person)
                else:
                    if not homeConnectionGraph.are_connected(person, currentGroup[0]):
                        homeConnectionGraph.add_edge(person, currentGroup[0])
                        currentGroup.append(person)
                        notInGroup.remove(person)

    return currentIteration

print(getIteration(graphNames, graph))

    # while (every person does not have true in the dictionary):
    #     for person in listOfPeople:
    #         if(currentGroup.size == 4):
    #             currentIteration.append(currentGroup)
    #             currentGroup.clear()

    #         # current group to put people into (person in spot 1 should be host)
    #         if (dictionary[person] == false):
    #             if currentGroup.size == 0:
    #                 currentGroup.append(person)
    #                 dictionary[person] = true
    #             else # we need to add a person to the current group that has not been to the host's house
    #                 if(not an edge between person and current host):
    #                     add edge between person and current host
    #                     currentGroup.append(person)
    #                     dictionary[person] = true

#     return currentIteration


# listOfIterations = []

# # if we have a clique, everyone has been to everybody's house
# if graph.omega() == list.size:
#     return finalIteration