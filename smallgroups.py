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

    while notInGroup:
        if fullBreak:
            break
        for person in listOfPeople:
            # check if person is a couple
            isCouple = False
            if "," in person:
                isCouple = True

            if peopleInGroup == m:
                temp = currentGroup.copy()
                currentIteration.append(temp)
                currentGroup.clear()
                peopleInGroup = 0

            # current group to put people into (person in spot 1 should be host)
            if person in notInGroup:
                if not currentGroup:
                    currentGroup.append(person)
                    notInGroup.remove(person)
                    peopleInGroup += 1
                    if isCouple:
                        peopleInGroup += 1
                else:
                    if not homeConnectionGraph.are_connected(person, currentGroup[0]):

                        # check if there is one spot left in the group and we try to
                        #   add a couple, then skip
                        if not (peopleInGroup == m-1 and isCouple):
                            homeConnectionGraph.add_edge(person, currentGroup[0])
                            currentGroup.append(person)
                            notInGroup.remove(person)
                            peopleInGroup += 1
                            if isCouple:
                                peopleInGroup += 1
                        else:
                            if len(notInGroup) == 1:
                                temp = currentGroup.copy()
                                currentIteration.append(temp)
                                currentGroup.clear()
                                currentGroup.append(person)
                                fullBreak = True
    
    # if there are left over people who did not fit in the last group
    if currentGroup:
        i = 0
        for person in currentGroup:
            currentIteration[m-i].append(person)
            i += 1

    return currentIteration

print(getIteration(graphNames, graph, m))


# listOfIterations = []

# # if we have a clique, everyone has been to everybody's house
# if graph.omega() == list.size:
#     return finalIteration