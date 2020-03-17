import sys
from igraph import *

m = 4

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

def getIteration(listOfPeople, homeConnectionGraph, m):

    # create list of iterations and list for storing groups of the current iteration
    notInGroup = listOfPeople.copy()
    currentIteration = []
    currentGroup = []
    peopleInGroup = 0
    fullBreak = False
    notConnectedToCurrentHost = []
    
    while notInGroup:
        # notConnectedToCurrentHost = notInGroup.copy()
        if fullBreak:
            break
        for person in notInGroup:
            
            # check if person is a couple
            isCouple = False
            if "," in person:
                isCouple = True

            # if current person is a couple and we only have one spot left in
            #   the group, then skip over them
            if (peopleInGroup == m-1 and isCouple):
                continue

            # if group size is full, add it to the iteration and clear the group
            if peopleInGroup == m:
                temp = currentGroup.copy()
                currentIteration.append(temp)
                currentGroup.clear()
                peopleInGroup = 0

            # if current group is empty, add current person to current group as host
            if not currentGroup:

                # if we have leftovers, don't add a host
                if len(notInGroup) < m:
                    fullBreak = True
                    break

                # else, add a host
                else:
                    currentGroup.append(person)
                    notInGroup.remove(person)
                    notConnectedToCurrentHost.clear()
                    notConnectedToCurrentHost = notInGroup.copy()
                    peopleInGroup += 1
                    if isCouple:
                        peopleInGroup += 1
            
            # if the current group has people in it, check for connections to host
            else:
                # if current person has NOT already been to the current host's house
                if not homeConnectionGraph.are_connected(person, currentGroup[0]):
                    
                    # add graph connection between person and current host storing
                    #   that the current person has now been to the current host's house
                    homeConnectionGraph.add_edge(person, currentGroup[0])

                    # add current person to the group
                    currentGroup.append(person)

                    # remove the current person from the list of ungrouped people
                    notInGroup.remove(person)

                    # add 1 to our people in group counter
                    peopleInGroup += 1

                    #if we have a couple, add another to our people in group counter
                    if isCouple:
                        peopleInGroup += 1
                else:
                    notConnectedToCurrentHost.remove(person)
                    if not notConnectedToCurrentHost:
                        # add current person to the group
                        currentGroup.append(person)

                        # remove the current person from the list of ungrouped people
                        notInGroup.remove(person)

                        # add 1 to our people in group counter
                        peopleInGroup += 1

                        #if we have a couple, add another to our people in group counter
                        if isCouple:
                            peopleInGroup += 1
    # if we have leftovers, add them to other lists
    if (notInGroup):
        i = 1
        for person in notInGroup:
            currentIteration[-i].append(person)
            i += 1

    return currentIteration

def makeGroups(listOfPeople, homeConnectionGraph, m):
    listOfIterations = []
    # if we have a clique, everyone has been to everybody's house
    while (graph.omega() != len(listOfPeople)):
        iteration = getIteration(listOfPeople, homeConnectionGraph, m)
        listOfIterations.append(iteration)
        print(iteration)
    return listOfIterations

makeGroups(graphNames, graph, m)

# 
# if graph.omega() == list.size:
#     return finalIteration