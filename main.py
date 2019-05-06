# Fichier principal à éxécuter. Contient le cas d'une population simple, avec un taux de synchronisation donné.

import random
from copy import deepcopy
import matplotlib.animation
import matplotlib.pyplot as plt
# TOOLS
from tools import *
# PATTERNS
from patterns import *

canclick = True


# RULES
def numberNeighbors(C, i, j):
    # assert(1<=i<=N and 1<=j<=N):'message'
    nbList = [C[i + 1, j], C[i + 1, j + 1], C[i + 1, j - 1], C[i - 1, j], C[i - 1, j + 1], C[i - 1, j - 1], C[
        i, j + 1], C[i, j - 1]]
    return np.count_nonzero(nbList)


def deathCondition(C, i, j):  # la cellule meurt si elle a plus de x voisins ou moins de y voisins
    x = 3  # Nombre maximal de voisins au dela duquel la cellule meurt

    y = 1  # Nombre minimal de voisins au dessus duquel la cellule meurt
    if numberNeighbors(C, i, j) > x or numberNeighbors(C, i, j) <= y:
        return True
    else:
        return False


def rebornCondition(C, i, j):  # la cellule nait si elle a z voisins
    z = 3  # Nombre de voisins qui font renaître la cellule
    if numberNeighbors(C, i, j) == z:
        return True
    else:
        return False


def update(t, C, sync, im=None):
    N = len(C)-2
    a = deepcopy(C)
    unstable = 0
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if random.random() <= sync: # the cell is updated with a probability depending on the synchronisation rate
                if C[i, j] == 0 and rebornCondition(C, i, j):
                    a[i, j] = 1
                elif C[i, j] != 0 and deathCondition(C, i, j):
                    a[i, j] = 0
            if C[i, j] != 0 and not deathCondition(C, i, j): # increments the age of living cells
                 a[i, j] = C[i, j] + 1
            if a[i, j] == 1 or (a[i, j] == 0 and C[i, j] != 0): # detects if the cell is unstable (revived or died)
                unstable += 1
    # print(t)
    # print(a)
    # print("count:", count(C))
    # print("mean age:", meanAge(C))
    # print("unstable:", unstable)
    C = a
    if im is not None:
        im.set_array(a)
    t += 1
    return a, unstable


# INTERACTION
def onclick(event, ax, fig, C):
    N = len(C)-2
    if canclick:
        if ax.in_axes(event):
            ax_pos = ax.transAxes.inverted().transform((event.x, event.y))
            i = N+1-int((ax_pos[1])*(N+2))
            j = int((ax_pos[0])*(N+2))
            C[i, j] = 1
            print(canclick)
            plt.imshow(C, interpolation="none", cmap="Blues")
            fig.canvas.draw()


# ANIMATION
def main1():
    # Grid & initial situation
    N = 100  # Dimension du 2D array, sans compter les bordures
    pop = 0.5 # proportion of living cells at the beginning
    sync = 0.3 # synchronisation rate : 0 = completely asynchronous (no updating) -> 1 = completely synchronous (basic simultaneous updating)

    C = np.zeros((N + 2, N + 2))  # le 2D array. 0: pas de cellule.1: cellule présente.
    C[1:N+1, 1:N+1] = randomGrid(N, pop)

    # Animation
    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = plt.imshow(C, interpolation="none", cmap="Blues")
    title = plt.title("")
    ani = matplotlib.animation.FuncAnimation(fig, func=update, fargs=(C, sync, im),
                                             repeat=False, interval=1)
    plt.show()


# ANALYSE
def main2():
    popList = np.linspace(0,1,11)
    nsteps = 100

    activityRes = np.zeros(11)
    densityRes = np.zeros(11)
    ageRes = np.zeros(11)
    for i in range(11):
        print("i =", i)
        # Grid & initial situation
        N = 100  # Dimension du 2D array, sans compter les bordures
        pop = popList[i] # proportion of living cells at the beginning
        sync = 0.3 # synchronisation rate : 0 = completely asynchronous (no updating) -> 1 = completely synchronous (basic simultaneous updating)

        C = np.zeros((N + 2, N + 2))  # le 2D array. 0: pas de cellule.1: cellule présente.
        C[1:N+1, 1:N+1] = randomGrid(N, pop)

        t = 0
        while t < nsteps:
            C = update(t, C, sync)[0]
            t += 1
        activityRes[i] = update(t, C, sync)[1]/N**2
        densityRes[i] = count(C)/N**2
        ageRes[i] = meanAge(C)
    plt.figure()
    plt.plot(popList, activityRes, 'r-')
    plt.title("Activity of cells after "+str(nsteps)+" steps")
    plt.figure()
    plt.plot(popList, densityRes, 'b-')
    plt.title("Density of living cells after "+str(nsteps)+" steps")
    plt.figure()
    plt.plot(popList, ageRes, 'g-')
    plt.title("Mean age of living cells after "+str(nsteps)+" steps")
    plt.show()

# MAIN
main2()


