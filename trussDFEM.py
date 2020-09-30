# Program for calculating the deformation of a simple truss via FEM

import numpy as np
import matplotlib.pyplot as plt
import os
from terminaltables import SingleTable as SingTab
from testModels import *
from plotsAndTables import *
from solver import *

def main():

    clearScreen = os.system('cls')
    clearScreen

    print('\n  -------------------------------- \
           \n  -- Truss Deformation with FEM -- \
           \n  -------------------------------- \
           \n  Author: Samuel Bryson')
    
    solve = 0; n = 0; choice = 0; nodeCount = 0
    elemCount = 0; bearCount = 0; loadCount = 0
    nodes = np.zeros((1,3)); elements = np.zeros((1,3)) 
    bearings = np.zeros((1,3)); loads = np.zeros((1,4))
    E = 210e9; A = 0.01; poiss = 0.3 # default values (vary depending on truss model)

    while solve != 1: # main loop
        clearScreen
        try:
            # clearScreen
            choice = float(input('\nOptions: \n  1 - Add node \n  2 - Add element \
            \n  3 - Add bearing \n  4 - Add load \n  5 - Update plot \n  6 - Edit model\
            \n  7 - Solve model \n  8 - Truss 1 \n  9 - Truss 2 \n 10 - Truss 3 \
            \n 11 - Truss 4 \n 12 - Truss 5 \n\n Selection: '))
        except ValueError:
            print ('\nPlease enter a number between 1 to 8!')
        if choice == 1:
            [nodes, nodeTable, nodeCount] = addNode(nodes, nodeCount)
        elif choice == 2:
            [elements, elemTable, elemCount] = addElement(elements, nodes, nodeTable, elemCount)
            elements = elements.astype(int) # consists only of element nr, node 1, node 1
        elif choice == 3: 
            [bearings, bearCount] = addBearing(bearings, nodes, bearCount, nodeTable)
        elif choice == 4: 
            [loads, loadCount] = addLoad(loads, nodes, loadCount, nodeTable)
        elif choice == 5:
            updatePlot(nodes, nodes, elements, bearings, loads, 0) # 0: not coming from solver (only plots basic structure)
        elif choice == 6:
            [E, A] = editTruss(nodes, nodeCount, nodeTable, elements, elemCount, elemTable)
        elif choice == 7:
            solve = 1
        elif choice == 8:
            [nodes, elements, bearings, loads, nodeTable, elemTable, A, E, poiss] = truss1()
            print ('\n Using values for truss 1.')
        elif choice == 9:
            [nodes, elements, bearings, loads, nodeTable, elemTable, A, E, poiss] = truss2()
            print ('\n Using values for truss 2.')
        elif choice == 10:
            [nodes, elements, bearings, loads, nodeTable, elemTable, A, E, poiss] = truss3()
            print ('\n Using values for truss 3.')
        elif choice == 11:
            [nodes, elements, bearings, loads, nodeTable, elemTable, A, E, poiss] = truss4()
            print ('\n Using values for truss 4.')
        elif choice == 12:
            [nodes, elements, bearings, loads, nodeTable, elemTable, A, E, poiss] = truss5()
            print ('\n Using values for truss 5.')
        choice = 0 # otherwise simply pressing "enter" without number input assumes previous option
    print("\n")
    print (SingTab(nodeTable, title = "Nodes").table)
    print (SingTab(elemTable, title = "Elements").table)

    solver(nodes, elements, bearings, loads, nodeTable, elemTable, A, E)

def addNode(nodes, nodeCount):
    newNode = np.zeros((1,3)); # node nr | x-coord | y-coord
    newNode[0,0] = nodeCount + 1
    print ('\nEnter x: ')
    newNode[0,1] = getNumber()
    print ('\nEnter y: ')
    newNode[0,2] = getNumber()
    if nodeCount == 0:
        nodes = newNode
    else:
        nodes = np.vstack((nodes, newNode))
    nodeTable = nodeTableFunc(nodes)
    nodeCount += 1
    print (SingTab(nodeTable, title = "Nodes").table)
    return [nodes, nodeTable, nodeCount]

def addElement(elements, nodes, nodeTable, elemCount):
    newElem = np.zeros((1,3)) # element nr | start node | end node
    print (SingTab(nodeTable, title = "Nodes").table)
    newElem[0,0] = elemCount + 1
    print ('\n Which nodes would you like to connect?\n\n Enter first node: ')
    newElem[0,1] = getNumber()
    print ('\n Enter second node: ')
    newElem[0,2] = getNumber()
    if elemCount == 0:
        elements = newElem
    else: 
        elements = np.vstack((elements, newElem))
    elemTable = elemTableFunc(elements)
    elemCount += 1
    print (SingTab(elemTable, title = "Elements").table)
    return [elements, elemTable, elemCount]

def addBearing(bearings, nodes, bearCount, nodeTable):
    newBear = np.zeros((1,4)) # bearing nr | node | orientation
    print (' Fixed bearing (1) or roller (2)?')
    newBear[0,0] = getNumber()
    print (SingTab(nodeTable, title = "Nodes").table)
    print (' \nPlace bearing at which node?')
    newBear[0,1] = getNumber()
    if newBear[0,0] == 1:
        print (' Is bearing at bottom (1) or top (2) of truss?')
        bearSet = getNumber()
        if bearSet == 1:
            newBear[0,2] = 1 # pointing upwards
        elif bearSet == 2:
            newBear[0,2] = 3 # downwards
    elif newBear[0,0] == 2:
        print (' Block vertical (1) or horizontal (2) movement?')
        bearSet = getNumber()
        if bearSet == 1:
            print (' Is bearing at bottom (1) or top (2) of truss?')
            bearSet = getNumber()
            if bearSet == 1:
                newBear[0,2] = 1 # upwards
            elif bearSet == 2:
                newBear[0,2] = 3 # downwards 
        elif bearSet == 2:
            print (' Is bearing at left (1) or right (2) of truss?')
            bearSet = getNumber()
            if bearSet == 1:
                newBear[0,2] = 4 # pointing right
            elif bearSet == 2:
                newBear[0,2] = 2 # pointing left
    if bearCount == 0:
        bearings = newBear
    else: 
        bearings = np.vstack((bearings, newBear))
    bearCount += 1
    return [bearings, bearCount]

def addLoad(loads, nodes, loadCount, nodeTable):
    newLoad = np.zeros((1,4)) # load nr | node | orientation | magnitude
    print ('\n List of nodes: \n', SingTab(nodeTable).table)
    newLoad[0,0] = loadCount + 1
    print ('\n To which node is the load attached? Enter node number: ')
    newLoad[0,1] = getNumber()
    print ('\n Enter load direction (up (1), left (2), down (3), right (4)):' )
    newLoad[0,2] = getNumber()
    print ('\n Enter magnitude: ')
    newLoad[0,3] = getNumber()
    if loadCount == 0:
        loads = newLoad
    else: 
        loads = np.vstack((loads, newLoad))
    loadCount += 1
    return [loads, loadCount]

def getNumber():
    errorstr = 'Please enter a number!'
    while True:
        try:
            num = float(input(' '))
            break
        except ValueError:
            print (errorstr)
    return num

def editTruss(nodes, nodeCount, elements, elemCount):
    print ('Enter Young\'s modulus E')
    E = getNumber()
    print ('Enter beam cross-sectional area A:')
    A = getNumber()
    return E, A

if __name__ == '__main__':
    main()