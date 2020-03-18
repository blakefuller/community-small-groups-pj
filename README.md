# Creating Community Small Groups
A work by: Trent Cowden and Blake Fuller

*Write an introduction to your work*

## Description
The problem is as follows: a large group of people get together and want to divide themselves into small groups for an activity, whether that be work groups, a Bible study, etc. In each small group a host is chosen, and all the other small group members meet at the host's house. Each week, the groups are reshuffled and new small group members meet at a new host's house. The question is, what is the minimum number of iterations (or times the small groups meet) such that every member of the large group of people will have been to every other member's house" Likewise, such the minimum number of iterations such that every member of the large group will have hosted every other member at least once?

As an additional issue, married couples are allowed to join the small groups. The couples will count as two people in terms of the size of the groups, but they will always need to be in the same small group.

To go about solving this problem, we created a Python program that reads a simple txt file with a list of the names (couples on one line separated by a comma), and runs an greedy algorithm that determines the minimum number of iterations and prints out the names of everyone in each small group in each iteration.

## Requirements
The dependencies to run this program are **Python 3.x** and **python-igraph version 0.8.0**

If you don't have Python 3 installed, refer to the Python [download](https://www.python.org/downloads/) page.

To install python-igraph, run **pip install python-igraph** in a terminal window.

## User Manual
To clone this repository, click on the green **Clone or download** button in the top right, copy the HTTPS link, then type **git clone *link*** (where *link* is what you copied) in a terminal window in the directory of wherever you want to to save the files. Type **cd community-small-groups-pj**.

Then to run the program, type **python3 smallgroups.py group1.txt *m*** (where *m* is the desired size of each small group). If *python3* isn't recognized as a command, try running just *python* instead.

## Reflection
*Write the reflection about getting the small groups in the minimum number of iterations, etc.*


