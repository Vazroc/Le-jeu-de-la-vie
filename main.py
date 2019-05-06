import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np
import random
import sys
from copy import deepcopy
'''
Le code n'est pas encore optimisé pour le cas ou on veut lancer 2 familles de cellules différentes sur le jeu de la vie.
'''

# PATTERNS DICTIONARY
glider = [[1, 0, 0],
          [0, 0, 1],
          [1, 1, 1]]


# GRID & INITIAL SITUATION
N = 50  # Dimension du 2D array

C = np.zeros((N + 2, N + 2))  # le 2D array. 0: pas de cellule.1: cellule présente.
C[1:4, 1:4] = glider
C[20:23, 20:23] = glider

canclick = True

t = 0


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
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if C[i, j] == 0 and rebornCondition(i, j):
                a[i, j] = 1
            if C[i, j] != 0:
                    if deathCondition(i, j):
                         a[i, j] = 0
                    else:
                        a[i, j] = C[i,j] + 1
    # print(a)
    print(t)
    print("count:", count())
    print("mean age:", meanAge())
    C = a
    im.set_array(a)
    t += 1


# TOOLS
def count():
    count = 0
    for i in range(1, N+1):
        for j in range(1, N+1):
            if C[i][j] != 0:
                count += 1
    return count


def meanAge():
    sum = 0
    count = 0
    for i in range(1, N+1):
        for j in range(1, N+1):
            if C[i][j] != 0:
                sum += C[i][j]
                count += 1
    if count != 0:
        return sum/count
    else:
        return 0





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

fig = plt.figure()
ax = fig.add_subplot(111)
im = plt.imshow(C, interpolation="none", cmap="Blues")

title = plt.title("")


ani = matplotlib.animation.FuncAnimation(fig, func=update,
                                             repeat=False, interval=50)
plt.show()