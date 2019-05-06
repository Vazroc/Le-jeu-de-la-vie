import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np
import random
import sys
from copy import deepcopy
# TOOLS
import tools
'''
Le code n'est pas encore optimisé pour le cas ou on veut lancer 2 familles de cellules différentes sur le jeu de la vie.
'''

# PATTERNS DICTIONARY
glider = [[1, 0, 0],
          [0, 0, 1],
          [1, 1, 1]]


# GRID & INITIAL SITUATION
N = 50  # Dimension du 2D array, sans compter les bordures

C = np.zeros((N + 2, N + 2))  # le 2D array. 0: pas de cellule.1: cellule présente.
C[1:4, 1:4] = glider
C[20:23, 20:23] = glider


canclick = True

# RULES
def numberNeighbors(i, j):
    # assert(1<=i<=N and 1<=j<=N):'message'
    nbList = [C[i + 1, j], C[i + 1, j + 1], C[i + 1, j - 1], C[i - 1, j], C[i - 1, j + 1], C[i - 1, j - 1], C[
        i, j + 1], C[i, j - 1]]
    return np.count_nonzero(nbList)


def deathCondition(i, j):  # la cellule meurt si elle a plus de x voisins ou moins de y voisins
    x = 3  # Nombre maximal de voisins au dela duquel la cellule meurt

    y = 1  # Nombre minimal de voisins au dessu duquels la cellule meurt
    if numberNeighbors(i, j) > x or numberNeighbors(i, j) <= y:
        return True
    else:
        return False


def rebornCondition(i, j):  # la cellule nait si elle a z voisins
    z = 3  # Nombre de voisins qui font renaître la cellule
    if numberNeighbors(i, j) == z:
        return True
    else:
        return False


def update(t):
    global C
    a = deepcopy(C)
    unstable = 0
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if C[i, j] == 0 and rebornCondition(i, j):
                a[i, j] = 1
            if C[i, j] != 0:
                    if deathCondition(i, j):
                         a[i, j] = 0
                    else:
                        a[i, j] = C[i,j] + 1
            if a[i, j] == 1 or (a[i, j] == 0 and C[i, j] != 0):
                unstable += 1
    print(t)
    # print(a)
    print("count:", count(C))
    print("mean age:", meanAge(C))
    print("unstable:", unstable)
    C = a
    im.set_array(a)
    t += 1


# INTERACTION
def onclick(event):
    global C
    if (canclick):
        if ax.in_axes(event):
            ax_pos = ax.transAxes.inverted().transform((event.x, event.y))
            i = N+1-int((ax_pos[1])*(N+2))
            j = int((ax_pos[0])*(N+2))
            C[i,j] = 1
            print(canclick)
            plt.imshow(C, interpolation="none", cmap="Blues")
            fig.canvas.draw()


# MAIN
fig = plt.figure()
ax = fig.add_subplot(111)
im = plt.imshow(C, interpolation="none", cmap="Blues")
title = plt.title("")
ani = matplotlib.animation.FuncAnimation(fig, func=update,
                                             repeat=False, interval=50)
plt.show()