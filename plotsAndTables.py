import numpy as np
import matplotlib.pyplot as plt
from terminaltables import SingleTable as SingTab


def updatePlot(nodes, nodesNew, elements, bearings, loads, fromSolver):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    alphaNew = 1
    if fromSolver == 1:
        alphaOrig = 0.2 # if coming from solver, set original truss to alpha = 0.3
        ax.plot(nodesNew[:,1], nodesNew[:,2], 'ok', markersize = 5) # plot nodes
    elif fromSolver == 0:
        alphaOrig = 1
    ax.plot(nodes[:,1], nodes[:,2], 'ok', markersize = 5, alpha = alphaOrig) # plot nodes

    if nodes[0,0] == 0:
        print ('\n At least add some nodes...')
        return
    maxes = np.zeros((2*np.shape(bearings)[0]))
    for i in range(0, np.shape(bearings)[0]):
        maxes[2*i-1] = nodes[int(bearings[i,1]-1),1]
        maxes[2*i] = nodes[int(bearings[i,1]-1),2]
    factor = max(maxes)/4 # multiplication factor for resizing
    if elements[0,0] != 0:
        for i in range(0, np.shape(elements)[0]): # plot elements (lines between connected nodes)
            pair = np.array([elements[i,1], elements[i,2]]).astype(int)
            ax.plot(nodes[pair-1, 1], nodes[pair-1, 2], 'k', alpha = alphaOrig)
    if fromSolver == 1:
        for i in range(0, np.shape(elements)[0]): # plot elements (lines between connected nodes)
            pair = np.array([elements[i,1], elements[i,2]]).astype(int)
            ax.plot(nodesNew[pair-1, 1], nodesNew[pair-1, 2], 'k', alpha = alphaNew)
    if bearings[0,0] != 0:
        for i in range(0, np.shape(bearings)[0]): 
            try:
                sinVal = np.sin((np.pi)*(bearings[i,2]-1)/2)
                cosVal = np.cos((np.pi)*(bearings[i,2]-1)/2)
            except IndexError: # if no bearings have been defined
                break
            plotBearing(bearings[i,0], nodes[int(bearings[i,1]-1),1], 
                        nodes[int(bearings[i,1]-1),2], bearings[i,2], 
                        ax, sinVal, cosVal, alphaOrig, factor)
    if fromSolver == 1:
        for i in range(0, np.shape(bearings)[0]): 
            try:
                sinVal = np.sin((np.pi)*(bearings[i,2]-1)/2)
                cosVal = np.cos((np.pi)*(bearings[i,2]-1)/2)
            except IndexError: # if no bearings have been defined
                break
            plotBearing(bearings[i,0], nodesNew[int(bearings[i,1]-1),1], 
                        nodesNew[int(bearings[i,1]-1),2], bearings[i,2], 
                        ax, sinVal, cosVal, alphaNew, factor)
    if loads[0,0] != 0:
        for i in range(0, np.shape(loads)[0]):
            try:
                sinVal = np.sin((np.pi)*(loads[i,2]-1)/2)
                cosVal = np.cos((np.pi)*(loads[i,2]-1)/2)
            except IndexError: # if no loads have been defined
                break
            plotLoad(nodesNew[int(loads[i,1]-1),1], nodesNew[int(loads[i,1]-1),2], sinVal, cosVal, ax, factor)
    if np.shape(nodes)[0] >= 2:
        plotAnnotations(nodesNew, elements, loads, ax, fromSolver)
    xleft, xright = (min(nodesNew[:,1])-factor*0.5, max(nodesNew[:,1])+factor*0.5)
    ybottom, ytop = (min(nodesNew[:,2])-factor*0.5, max(nodesNew[:,2])+factor*0.5)
    ax.set_xlim(xleft, xright)
    ax.set_ylim(ybottom, ytop)
    ax.set_aspect('equal')
    plt.show()
    if fromSolver == 0:
        print ('\nClose plot to continue!')
    elif fromSolver == 1:
        print ('\nGoodbye!')

    return

def plotAnnotations(nodes, elements, loads, ax, fromSolver):
    nodeLabels = [nodes[i,0].astype(int) for i in range(np.shape(nodes)[0])]
    loadLabels = [repr(loads[i,3]) + ' N' for i in range(np.shape(loads)[0])]
    # for label, x, y in zip(nodeLabels, nodes[:,1], nodes[:,2]):
    #     ax.annotate(
    #         label,
    #         xy=(x, y), xytext=(-3, 15), 
    #         textcoords = 'offset points', ha = 'right', va = 'bottom',
    #         arrowprops = dict(arrowstyle = '-', connectionstyle = 'arc3, rad=0.3'))
    # if fromSolver == 0:
    elemLabels = [elements[i,0].astype(int) for i in range(np.shape(elements)[0])]
    for i in range(0, np.shape(elements)[0]):
        x1 = nodes[int(elements[i,1]-1),1]
        y1 = nodes[int(elements[i,1]-1),2]
        x2 = nodes[int(elements[i,2]-1),1]
        y2 = nodes[int(elements[i,2]-1),2]
        ax.annotate(
            elemLabels[i],
            xy=(0.5*(x2+x1), 0.5*(y2+y1)), xytext=(-3, 15), color = 'b',
            textcoords = 'offset points', ha = 'right', #va = 'bottom',
            arrowprops = dict(arrowstyle = '-', connectionstyle = 'arc3, rad=0.3'))
    if loads[0,0] != 0:
        for label, x, y in zip(loadLabels, 
                               nodes[(loads[:,1]-1).astype(int),1], 
                               nodes[(loads[:,1]-1).astype(int),2]):
            ax.annotate(
                label,
                xy=(x, y), xytext=(5, -5), color = 'r',
                textcoords = 'offset points', ha = 'left', va = 'top')

def plotBearing(bearType, bearX, bearY, orientation, ax, sinVal, cosVal, alpha, factor):
    sinVal *= factor
    cosVal *= factor
    xTriangle = [-0.12,0,0.12] # coordinates for main triangle shape
    yTriangle = [-0.18,0,-0.18]
    xBase1 = [-0.16,0.16]
    yBase1 = [-0.18, -0.18]
    xBase2 = [-0.16,0.16]
    yBase2 = [-0.2, -0.2]

    ax.plot(bearX + np.multiply(cosVal, xTriangle) - np.multiply(sinVal, yTriangle), 
            bearY + np.multiply(sinVal, xTriangle) + np.multiply(cosVal, yTriangle), alpha = alpha, color = 'k')
    ax.plot(bearX + np.multiply(cosVal, xBase1) - np.multiply(sinVal, yBase1), 
            bearY + np.multiply(sinVal, xBase1) + np.multiply(cosVal, yBase1), alpha = alpha, color = 'k')
    ax.set_aspect('equal')

    if bearType == 1:
        for i in np.arange(0,1,0.1):
            ax.plot(bearX + np.multiply(cosVal, [0.16-(i)*0.32, 0.16-(i+0.1)*0.32]) - np.multiply(sinVal, [-0.18, -0.2]), 
                    bearY + np.multiply(sinVal, [0.16-(i)*0.32, 0.16-(i+0.1)*0.32]) + np.multiply(cosVal, [-0.18, -0.2]), 
                    alpha = alpha, color = 'k')
    elif bearType == 2:
        ax.plot(bearX + np.multiply(cosVal, xBase2) - np.multiply(sinVal, yBase2), 
                bearY + np.multiply(sinVal, xBase2) + np.multiply(cosVal, yBase2), 
                    alpha = alpha, color = 'k')
        for i in np.arange(0,1,0.1):
            ax.plot(bearX + np.multiply(cosVal, [0.16-(i)*0.32, 0.16-(i+0.1)*0.32]) - np.multiply(sinVal, [-0.2, -0.22]), 
                    bearY + np.multiply(sinVal, [0.16-(i)*0.32, 0.16-(i+0.1)*0.32]) + np.multiply(cosVal, [-0.2, -0.22]), 
                    alpha = alpha, color = 'k')
    return

def plotLoad(xLoad, yLoad, sinVal, cosVal, ax, factor):
    sinVal *= 0.5*factor
    cosVal *= 0.5*factor
    xStem = [0,0]
    yStem = [0,0.4]
    xHead = [-0.05, 0, 0.05]
    yHead = [0.32, 0.4, 0.32] # pulls (0,0) upwards for direction = 1
    ax.plot(xLoad, yLoad, 'or')
    ax.plot(xLoad + np.multiply(cosVal, xStem) - np.multiply(sinVal, yStem), 
            yLoad + np.multiply(sinVal, xStem) + np.multiply(cosVal, yStem), 'r')
    ax.plot(xLoad + np.multiply(cosVal, xHead) - np.multiply(sinVal, yHead), 
            yLoad + np.multiply(sinVal, xHead) + np.multiply(cosVal, yHead), 'r')
    return

def nodeTableFunc(nodes):
    rows = [['Node Nr', '(x, y)']]
    for i in range(0, len(nodes)):
        rows.append([int(nodes[i,0]), ('(' + str(nodes[i,1]) + ', ' + str(nodes[i,2]) + ')')])
    SingTab.table_data = rows
    return SingTab.table_data

def elemTableFunc(elements):
    rows = [['Element Nr', 'From', 'To']]
    for i in range(0, len(elements)):
        rows.append([int(elements[i,0]), int(elements[i,1]), int(elements[i,2])])
    SingTab.table_data = rows
    return SingTab.table_data

def stressTableFunc(elements, strain, stress):
    stressAdj = stress/10**6
    strainAdj = strain*10**6
    rows = [['Element Nr', 'Strain', 'S11 Stress']]
    for i in range(0, len(elements)):
        rows.append([int(elements[i,0]),  str(round(strainAdj[i,0], 3)) + 'E-06', str(round(stressAdj[i,0], 3)) + 'E+06'])
    SingTab.table_data = rows
    return SingTab.table_data