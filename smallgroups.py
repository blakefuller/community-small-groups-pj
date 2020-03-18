import sys
from igraph import *
import random 

m = 5

#read from file and store names as a list of lists
fp = open("group2.txt", "r")
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
    numCouples = 0
    for person in listOfPeople:
        if ',' in person:
            numCouples += 1

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

                #edge case for if we have one spot left and one or more couples left in notInGroup
                if numCouples == len(notInGroup):
                    fullBreak = True
                    break

                #if we're skipping over a couple, remove them from notConnectedToCurrentHost
                if person in notConnectedToCurrentHost:
                    notConnectedToCurrentHost.remove(person)
                continue

            # if current group is empty, add current person to current group as host
            if not currentGroup:

                # if we have leftovers, don't add a host
                if (len(notInGroup) + numCouples) < m:
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
                        numCouples -= 1
            
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

                    # remove current person from list of people not connected to host
                    notConnectedToCurrentHost.remove(person)

                    #if we have a couple, add another to our people in group counter
                    if isCouple:
                        peopleInGroup += 1
                        numCouples -= 1
                else:
                    if person in notConnectedToCurrentHost:
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
                            numCouples -= 1

            # if group size is full, add it to the iteration and clear the group
            if peopleInGroup == m:
                temp = currentGroup.copy()
                currentIteration.append(temp)
                currentGroup.clear()
                peopleInGroup = 0
    # if we have leftovers, add them to other lists
    if (notInGroup):
        i = 1
        for person in notInGroup:
            # currentIteration[-i].append(person)
            # i += 1
            if i < len(currentIteration):
                currentIteration[-i].append(person)
                homeConnectionGraph.add_edge(person, currentIteration[-i][0])
            else:
                i = 0
            i += 1

    return currentIteration

def makeGroups(listOfPeople, homeConnectionGraph, m):
    listOfIterations = []
    # if we have a clique, everyone has been to everybody's house
    while (graph.omega() != len(listOfPeople)):
        # listOfPeople.append(listOfPeople[0])
        # listOfPeople.remove(listOfPeople[0])

        # probably running infinite loops because just 2 people never get connected
        random.shuffle(listOfPeople)

        iteration = getIteration(listOfPeople, homeConnectionGraph, m)
        listOfIterations.append(iteration)
        print(iteration)
    return listOfIterations

print(len(makeGroups(graphNames, graph, m)))

# print(graph)