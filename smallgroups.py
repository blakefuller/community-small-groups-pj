# imports
import sys
from igraph import *

# get filename and group size from command line
fileName = sys.argv[1]
m = int(sys.argv[2])

# group sizes of 3 or less are not allowed. 2 couples will never be connected if group size is 3 or less
if (m <= 3):
    print('ERROR: minimium group size is 4. This is because 2 couples will never be connected if group size is 3 or less.')
    sys.exit()

# read from file and store names as a list of lists
# change name of file to test groups ('group1.txt,' 'group2.txt', or 'group3.txt')
fp = open(fileName, "r")
lines = fp.readlines()
names = []
graphNames = []
for line in lines:
    names.append(line.rstrip("\n").split(","))
    graphNames.append(line.rstrip("\n"))

# set up graph with each name as a node (couple is one node)
homeConnectionsGraph = Graph()
homeConnectionsGraph.add_vertices(graphNames)

# function for getting a single iteration of groups
# PARAMETERS: a list of all the people, the graph of connections between them,
#   and the group size
def getIteration(listOfPeople, homeConnectionGraph, m):

    # full iteration for this instance of a list of people, add to as we go through
    currentIteration = []

    # list of all people who don't have a group
    ungroupedPeople = listOfPeople.copy()
    
    # keeping track of the current group that we're on (gets reset after each new group
    #   is added)
    currentGroup = []
    peopleInCurrentGroup = 0

    # variable for if we need to break out of our while loop and add leftovers
    #   becomes true if either there is one spot left and only a couple is left, or 
    #   the total number of ungrouped people isn't enough to form a group
    fullBreak = False

    # list of people who aren't connected to current. if this is empty, we have to add
    # someone to the current group who is already connected to host (not ideal)
    notConnectedToCurrentHost = []

    #number of couples in current list of people
    numUngroupedCouples = 0

    #get number of couples
    for person in listOfPeople:
        if ',' in person:
            numUngroupedCouples += 1

    while ungroupedPeople:
        # checking if we've reached one of the above mentioned situations and need to break
        #   out of loop to add leftovers
        if fullBreak:
            break

        #go through all ungrouped people
        for person in ungroupedPeople:
            
            # check if person is a couple (affects rest of code if they are)
            isCouple = False
            if "," in person:
                isCouple = True

            # EDGE CASE: if current person is a couple and we only have one spot left in
            #   the group, then skip over them
            if (peopleInCurrentGroup == m-1 and isCouple):

                #EDGE CASE: for if we have one spot left and one or more couples left in ungroupedPeople
                if numUngroupedCouples == len(ungroupedPeople):
                    fullBreak = True
                    break

                # if we're skipping over a couple, remove them from notConnectedToCurrentHost
                if person in notConnectedToCurrentHost:
                    notConnectedToCurrentHost.remove(person)
                continue

            # if current group is empty, add current person to current group as host
            #   note: host is always spot 0 in current group list
            if not currentGroup:

                # if the number of people left isn't enough to form a full group, exit the 
                #   while loop so we can add leftovers to other groups
                if (len(ungroupedPeople) + numUngroupedCouples) < m:
                    fullBreak = True
                    break

                # else, add a host
                else:

                    # add host to group and remove them from ungrouped people
                    currentGroup.append(person)
                    ungroupedPeople.remove(person)

                    # reset people who are connected to current host
                    notConnectedToCurrentHost.clear()
                    notConnectedToCurrentHost = ungroupedPeople.copy()

                    # add one to people in the current group
                    peopleInCurrentGroup += 1

                    # add another if it's a couple and remove one from the number of ungrouped couples
                    if isCouple:
                        peopleInCurrentGroup += 1
                        numUngroupedCouples -= 1
            
            # if we already have a host, check for connections to host
            # ideally, we want to add a person who doesn't have a connection to
            # the host, but we might have to
            else:
                # if current person has NOT already been to the current host's house
                if not homeConnectionGraph.are_connected(person, currentGroup[0]):
                    
                    # add graph connection between person and current host storing
                    #   that the current person has now been to the current host's house
                    homeConnectionGraph.add_edge(person, currentGroup[0])

                    # add current person to the current group
                    currentGroup.append(person)

                    # remove the current person from the list of ungrouped people
                    ungroupedPeople.remove(person)

                    # remove current person from list of people not connected to host
                    notConnectedToCurrentHost.remove(person)

                    # add 1 to our people in group counter
                    peopleInCurrentGroup += 1

                    # add another if it's a couple and remove one from the number of ungrouped couples
                    if isCouple:
                        peopleInCurrentGroup += 1
                        numUngroupedCouples -= 1
                
                #don't add them if they already have a connection
                else:
                    # EDGE CASE: if we eventually have tried adding all remaining people 
                    #   but all have connections to host, add a person who already 
                    #   has a connection to the host and keep going 
                    if person in notConnectedToCurrentHost:
                        notConnectedToCurrentHost.remove(person)

                    # this is where we add a person even if they have a connection, i.e.
                    #   the list of people who are not connected to the host is empty
                    if not notConnectedToCurrentHost:
                        # add current person to the group
                        currentGroup.append(person)

                        # remove the current person from the list of ungrouped people
                        ungroupedPeople.remove(person)

                        # add 1 to our people in group counter
                        peopleInCurrentGroup += 1

                        # add another if it's a couple and remove one from the number of ungrouped couples
                        if isCouple:
                            peopleInCurrentGroup += 1
                            numUngroupedCouples -= 1

            # if group size is full, add it to the iteration and clear the group/group size counter
            if peopleInCurrentGroup == m:
                temp = currentGroup.copy()
                currentIteration.append(temp)
                currentGroup.clear()
                peopleInCurrentGroup = 0

    # if we have leftovers, add them to other lists
    if (ungroupedPeople):
        i = 1
        for person in ungroupedPeople:
            if i < len(currentIteration):
                currentIteration[-i].append(person)
                homeConnectionGraph.add_edge(person, currentIteration[-i][0])
            else:
                i = 0
            i += 1

    return currentIteration

# function for making a list of all the iterations
# PARAMETERS: a list of all the people, the graph of connections between them,
#   and the group size
def makeGroups(listOfPeople, homeConnectionGraph, m):

    # list to store all the iterations of groups
    listOfIterations = []

    # counter to keep track of how many iterations
    iterationNumber = 0

    # if we have a clique, everyone has been to everybody's house
    while (homeConnectionsGraph.omega() != len(listOfPeople)):

        #reshuffling the order of the people so that the first person isn't
        #   a host every time
        listOfPeople.append(listOfPeople[0])
        listOfPeople.remove(listOfPeople[0])

        # get one iteration
        iteration = getIteration(listOfPeople, homeConnectionGraph, m)

        # add that iteration to the list of all iterations
        listOfIterations.append(iteration)

        # add one to iteration number 
        iterationNumber += 1

        #print each iteration
        print(f'iteration number {iterationNumber}: {iteration}\n')

    return listOfIterations

#PRINTING FOR TESTING

# print total number of iterations
print(f'total iterations: {len(makeGroups(graphNames, homeConnectionsGraph, m))}')

# print size of largest clique in the graph
print(f'size of largest clique (should be total size of people if program is working): {homeConnectionsGraph.omega()}')

# print whole unformatted list of lists
# print((makeGroups(graphNames, homeConnectionsGraph, m)))

# print the graph and all its nodes. use for showing whether every connection
#   has actually been made
# print(homeConnectionsGraph)

