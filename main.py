import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np
import random
import sys
from copy import deepcopy
import keyboard  # using module keyboard
'''
Le code n'est pas encore optimisé pour le cas ou on veut lancer 2 familles de cellules différentes sur le jeu de la vie.
'''
N = 50  # Dimension du 2D array

C = np.zeros((N + 2, N + 2))  # le 2D array. 0: pas de cellule.1: cellule présente.

x = 3  # Nombre maximal de voisins au dela duquel la cellule meurt

y = 1  # Nombre minimal de voisins au dessu duquels la cellule meurt

z = 3  # Nombre de voisins qui font renaître la cellule

canclick = True


glider = [[0, 0, 1],
          [1, 1, 0],
          [1, 1, 1]]
C[1:4,1:4] = glider




def NumberNeighbors(i, j):
    # assert(1<=i<=N and 1<=j<=N):'message'
    return C[i + 1, j] + C[i + 1, j + 1] + C[i + 1, j - 1] + C[i - 1, j] + C[i - 1, j + 1] + C[i - 1, j - 1] + C[
        i, j + 1] + C[i, j - 1]


def DeathCondition(i, j):  # la cellule meurt si elle a plus de x voisins ou moins de y voisins
    if NumberNeighbors(i, j) > x or NumberNeighbors(i, j) <= y:
        return True
    else:
        return False


def RebornCondition(i, j):  # la cellule nait si elle a z voisins
    if NumberNeighbors(i, j) == z:
        return True
    else:
        return False









def update(t):
    global C
    a  = deepcopy(C)
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if DeathCondition(i, j):
                a[i, j] = 0
            #if RebornCondition(i, j):
                #a[i, j] = 1
    print(a)
    C =a
    im.set_array(a)
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
                                             repeat=False, interval=100)
plt.show()
