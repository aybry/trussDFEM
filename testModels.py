import numpy as np
from plotsAndTables import nodeTableFunc, elemTableFunc

# NODES
# node nr | x-coord | y-coord

# ELEMENTS
# element nr | start node | end node

# BEARINGS
# bearing type | node | orientation

# LOADS
# load nr | node | orientation | magnitude

def truss1():
    nodes = np.array([[1,0.,0.], [2,12.,0.], [3,2*12.,0.], [4,3*12.,0.], [5,4*12.,0.],
                      [6,12.,-9.], [7,2*12.,-9.], [8,3*12.,-9.]])
    nodeTable = nodeTableFunc(nodes)
    elements = np.array([[1,1,2], [2,2,3], [3,3,4], [4,4,5], [5,1,6], [6,6,7], [7,7,8], [8,8,5],
                         [9,2,6], [10,3,7], [11,4,8], [12,6,3], [13,3,8]])
    elemTable = elemTableFunc(elements)
    bearings = np.array([[1,1,1], [2,5,1]])
    loads = np.array([[1,2,3,100000], [2,3,3,200000], [3,4,3,300000]])
    E = 2e11; A = 0.01; poiss = 0.3 
    return [nodes, elements, bearings, loads, nodeTable, elemTable, A, E, poiss]

def truss2():
    nodes = np.array([[1,0,0], [2,12,6], [3,0,4], [4,4,4.666667], [5,9,5.5], [6,7,3.5]]) 
    nodeTable = nodeTableFunc(nodes)
    elements = np.array([[1,1,6], [2,6,2], [3,2,5], [4,5,6], [5,6,4], [6,4,3], [7,5,4], [8,4,1]]) 
    elemTable = elemTableFunc(elements)
    bearings = np.array([[1,1,4], [1,3,4]])
    loads = np.array([[1,2,3,50000]])
    E = 2e11; A = 0.01; poiss = 0.3 
    return [nodes, elements, bearings, loads, nodeTable, elemTable, A, E, poiss]

def truss3():
    nodes = np.array([[1,0,0], [2,2,0], [3,4,0], [4,6,0], [5,1,0], [6,5,0], [7,3,2],
                      [8,2.5,1], [9,3.5,1], [10,1.5,1], [11,4.5,1], [12,0.75,0.5],
                      [13,2.25,1.5], [14,3.75,1.5], [15,5.25,0.5]]); nodeTable = nodeTableFunc(nodes)
    elements = np.array([[1,1,5], [2,5,2], [3,2,8], [4,8,7], [5,7,9], [6,9,3], [7,3,6], [8,6,4],
                         [9,1,12], [10,10,13], [11,7,14], [12,11,15], [13,5,10], [14,10,2], [15,10,8],
                         [16,9,11], [17,11,3], [18,11,6], [19,12,10], [20,13,7], [21,14,11], [22,15,4],
                         [23,5,12], [24,8,13], [25,9,14], [26,6,15]]); elemTable = elemTableFunc(elements)
    bearings = np.array([[1,1,1], [1,4,1]])
    loads = np.array([[1,7,3,500000], [2,10,3,500000], [3,11,3,500000]])
    E = 2e11; A = 0.1; poiss = 0.3
    return [nodes, elements, bearings, loads, nodeTable, elemTable, A, E, poiss]

def truss4(): # 6 nodes, fixed/roller bearings
    nodes = np.array([[1,0.,0.], [2,4.,0.], [3,2.,1.], [4,0.,2.], [5,4.,2.], [6,2.,3.]]); nodeTable = nodeTableFunc(nodes)
    elements = np.array([[1,1,3], [2,1,4], [3,3,2], [4,2,5], [5,5,6],
                        [6,6,3], [7,6,4], [8,4,3], [9,5,3]]); elemTable = elemTableFunc(elements)
    bearings = np.array([[1,1,1], [2,2,1]])
    loads = np.array([[1,3,3,100000]])
    E = 210e9; A = 0.001; poiss = 0.3
    return [nodes, elements, bearings, loads, nodeTable, elemTable, A, E, poiss]

def truss5():
    nodes = np.array([[1,0.,0.], [2,16.*12,0.], [3,16.*12,12.*12], [4,32.*12,0.], [5,32.*12,12.*12]]); nodeTable = nodeTableFunc(nodes)
    elements = np.array([[1,1,3], [2,1,2], [3,2,3], [4,3,5], [5,3,4], [6,2,5], [7,2,4], [8,4,5]]); elemTable = elemTableFunc(elements)
    bearings = np.array([[1,1,1], [1,4,1]])
    loads = np.array([[1,2,3,100], [2,5,4,50]])
    E = 3e4; A = 10; poiss = 0.3 # imperial
    # compare: http://people.duke.edu/~hpgavin/cee421/truss-method.pdf
    return [nodes, elements, bearings, loads, nodeTable, elemTable, A, E, poiss]