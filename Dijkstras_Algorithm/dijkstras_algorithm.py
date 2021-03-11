# -*- coding: UTF-8 -*-

import csv
import sys

def printPath(src,varList,distDict): #function for printing the least costh path and with src node, variable list and least costh&path dictionary as input
    print("Shortest path tree for node "+src+":")
    path = ""
    lis = []
    for index in range(0,len(varList)):
        if src == varList[index]:
            pass
        else:
            lis.append(distDict[varList[index]][-1])
    lis = sorted(lis,key=len) #sorting the shortest path by length
    for index in range(0,len(lis)):
        path += lis[index]+", "
    print(path[:-2])
    path = ""
    print("Costs of least-cost paths for node "+src+":")
    for index in range(0,len(varList)):
        path+= (varList[index]+":"+str(distDict[varList[index]][0])+", ")
    print(path[:-2]) #printing distance of all nodes from source node
    
def dijAlgol(src,varList,costDict): #function for generating least cost&path dictionary with src node, list of nodes and costs as input
    node = src
    distDict = {}
    for num in range(0,len(varList)):
        distDict[varList[num]] = [] #dictionary which holds variable as key and least cost from source & path in later steps
    firstBool = True
    least = [9999]

    for num in range(0,len(varList)):
        index = varList.index(varList[num])
        distDict[varList[num]] = [costDict[node][index],node+varList[num]] #updating dictinary with distance from source to other nodes and with path
        if int(least[0]) > int(distDict[varList[num]][0]) and int(distDict[varList[num]][0])!=0:
            least = [distDict[varList[num]][0],src] #finding variable with least cost from source
    for num in range(0,len(varList)):
        if least[-1] not in node:
            node += least[-1] #appending next least variabe to Node
        if len(node) == len(varList):
            break
        cost = int(least[0])
        least = [9999]
        for num1 in range(0,len(varList)):
            index = varList.index(varList[num1])
            if cost+int(costDict[node[-1]][index]) <int(distDict[varList[num1]][0]): #comparing present cost with new cost
                distDict[varList[num1]] = [cost+int(costDict[node[-1]][index]), distDict[node[-1]][-1]+varList[num1]] #updating least cost and path when new cost is less than old cost
            if(int(least[0]) > int(distDict[varList[num1]][0]) and varList[num1] not in node ):
                least = [distDict[varList[num1]][0],varList[num1]] #find next least cost from source
        
    printPath(src,varList,distDict) 
    return distDict
        
with open(sys.argv[1],mode='r') as csvFile:
    read = csv.reader(csvFile, delimiter = ',')
    firstBool = True
    costDict = {}
    lis = list()
    for row in read:
        if firstBool == True:
            for index in range(1,len(row)):
                lis.append(row[index]) #taking variables from csv to list
            firstBool = False
        else:
            for index in range(1,len(row)):
                if row[0] not in costDict:
                    costDict[row[0]] = [row[index]]
                else:
                    costDict[row[0]].append(row[index]) #appending costs to dictionary with variable as key
    counter = 0
    print(lis)
    while(True):
        src = input("Please, provide the node's name: ".format())
        if src not in lis: #if the given node is not in csv, asking for 2 more times for correct input
            print("Wrong Input node given")
            counter += 1
        else:
            dijAlgol(src,lis,costDict) 
            break
        if counter == 3:
            print("Input given wrongly three times. Exiting. . .")
            break

        
    
            
            
