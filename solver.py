import numpy as np
from numpy.linalg import solve as npsolve
from terminaltables import SingleTable as SingTab
from plotsAndTables import *

def solver(nodes, elements, bearings, loads, nodeTable, elemTable, A, E):

    np.set_printoptions(precision = 4) # how many decimal places

    print ('\n -------------\
           \n -- Results --\
           \n -------------')

    # print AscTab(nodeTable).table
    # print AscTab(elemTable).table
    Eprint = E/(10**9)
    print ('\nYoung\'s modulus: E = ' + str(Eprint) + 'e9')
    print ('Cross-sectional area: A =', A)

    elemNum = np.shape(elements)[0]
    nodeNum = np.shape(nodes)[0]
    Kl = np.zeros((4, 4, elemNum)) # initialise local (element) stiffness matrix
    lengths = np.zeros((elemNum,1)) # initialise vector of element lengths for stress()

    F = np.zeros(2*nodeNum) # initialise load vector
    U = np.zeros(2*nodeNum) # initialise displacement vector
    K = np.zeros((2*nodeNum, 2*nodeNum)) # intitalise global stiffness matrix

    for i in range(0, elemNum):
        x1 = nodes[(elements[i,1]-1).astype(int),1]
        y1 = nodes[(elements[i,1]-1).astype(int),2]
        x2 = nodes[(elements[i,2]-1).astype(int),1]
        y2 = nodes[(elements[i,2]-1).astype(int),2]
        elemLength = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        lengths[i,0] = elemLength
        c = (x2 - x1) / elemLength
        s = (y2 - y1) / elemLength
        # element stiffness matrix
        Kl[:,:,i] = [[c**2, c*s, -c**2, -c*s],
                     [c*s, s**2, -c*s, -s**2],
                     [-c**2, -c*s, c**2, c*s],
                     [-c*s, -s**2, c*s, s**2]]
        Kl[:,:,i] = np.multiply(1/elemLength, Kl[:,:,i])

        node1 = elements[i,1]
        node2 = elements[i,2]

        first = (2*node1 - 2).astype(int) # separating nodes into X, Y local
        second = (2*node1 - 1).astype(int)
        third = (2*node2 - 2).astype(int)
        fourth = (2*node2 - 1).astype(int)

        # global stiffness matrix: add DOF from elements
        K[first:second+1, first:second+1] += Kl[0:2,0:2,i]
        K[first:second+1, third:fourth+1] += Kl[0:2,2:4,i]
        K[third:fourth+1, first:second+1] += Kl[2:4,0:2,i]
        K[third:fourth+1, third:fourth+1] += Kl[2:4,2:4,i]

    for i in range(0, np.shape(bearings)[0]):
        # adjust stiffness matrix for bearings
        # this way leaves room to solve for reaction forces at a later date!
        node = bearings[i,1]
        first = (2*node - 2).astype(int) # separating nodes into X, Y local
        second = (2*node - 1).astype(int)
        if bearings[i,0] == 1:
            K[first, first] += 1e32
            K[second, second] += 1e32
        elif bearings[i,0] == 2:
            K[first, first] += (bearings[i,2] + 1) % 2 * 1e30 # if odd, add 1e30
            K[second, second] += (bearings[i,2]) % 2 * 1e30 # if even, add 1e30

    for i in range(0, np.shape(loads)[0]):
        # establish load vector
        node = loads[i,1]
        first = (2*node - 2).astype(int) # separating nodes into X, Y local
        second = (2*node - 1).astype(int)
        sinVal = np.sin((np.pi)*(loads[i,2]-1)/2)
        cosVal = np.cos((np.pi)*(loads[i,2]-1)/2)
        F[first] = - sinVal * loads[i,3]
        F[second] = cosVal * loads[i,3]

    K = np.multiply(E*A, K) # finalise stiffness matrix with E*A

    U = npsolve(K, F) # solve for displacements 

    for i in range(0, np.shape(U)[0]):
        if np.abs(U[i]) < 1e-12:
            U[i] = 0 # change ~0 to =0 for clarity
        if np.abs(F[i]) < 1e-12:
            F[i] = 0

    multiplier = 100
    nodesNew = np.zeros(np.shape(nodes)) + nodes
    nodesNewPlot = np.zeros(np.shape(nodes)) + nodes
    
    for i in range(0, np.shape(U)[0]):
        nodesNew[i//2, i%2+1] += U[i] # new coordinates of nodes after deformation
        nodesNewPlot[i//2, i%2+1] += U[i] * multiplier # exaggerated deformations for plotting

    # print '\nForce vector F = \n', F
    # print '\nGlobal stiffness matrix U = \n', K
    # print '\nDisplacement vector U =\n', U
    print ('\nGraph displacement scale factor: ', multiplier)

    stress(nodesNew, lengths, elements, bearings, loads, E)
    updatePlot(nodes, nodesNewPlot, elements, bearings, loads, 1) # 1: coming from solver (plots original + deformed)

    return

def stress(nodesNew, lengths, elements, bearings, loads, E):
    # initialise vector of element lengths
    lengthsNew = np.zeros((np.shape(elements)[0],1)) 
    # initialise vector of strain and stress in elements
    strain = np.zeros(np.shape(elements)[0])
    stress = np.zeros(np.shape(elements)[0])

    for i in range(0, np.shape(elements)[0]):
        xN1 = nodesNew[(elements[i,1]-1).astype(int), 1]
        yN1 = nodesNew[(elements[i,1]-1).astype(int), 2]
        xN2 = nodesNew[(elements[i,2]-1).astype(int), 1]
        yN2 = nodesNew[(elements[i,2]-1).astype(int), 2]
        lengthsNew[i] = np.sqrt((xN2 - xN1)**2 + (yN2 - yN1)**2)

    # strain = change in length by original length
    strain = (lengthsNew - lengths) / lengths

    # stress = strain multiplied by Young's modulus 
    stress = np.multiply(E, strain)
    
    stressTable = SingTab(stressTableFunc(elements, strain, stress), title = "Strain and Stress")
    stressTable.justify_columns[1] = stressTable.justify_columns[2] = 'right'
    print ("\n")
    print(stressTable.table) 
    return
