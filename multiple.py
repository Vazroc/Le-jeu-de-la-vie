import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np
import random
import sys
from copy import deepcopy
import keyboard  # using module keyboard

'''
Le code n'est pas encore optimisé pour le cas ou on veut lancer n familles quelconques de cellules différentes sur le jeu de la vie.
'''
N = 60  # Dimension du 2D array

NPopu=2 #nombre de populations

C = np.array([[[0 for k in range(NPopu)] for i in range(N+2)] for j in range(N+2)]) # le 2D array. 0: pas de cellule.1: cellule présente.

x = 3  # Nombre maximal de voisins au dela duquel la cellule meurt

y = 1  # Nombre minimal de voisins au dessu duquels la cellule meurt

z = 3  # Nombre de voisins qui font renaître la cellule

canclick = True

#Conditions d'initialisation:
C[1:N//2,1:N//2]=np.array([[[1,0]for i in range(1,N//2)] for j in range(1,N//2)]) #La Population 1 occupe le quartier haut gauche

C[N//2:N+1,N//2:N+1]=np.array([[[0,1]for i in range(N//2,N+1)] for j in range(N//2,N+1)]) #la Population 2 occupe le quartier bas droit



# Pour plot, on ne peut pas le faire directement avec C, on crée un Grid avec les valeurs: 0 si case vide, 1 si case population 1, 2 si case population 2, etc...
def convert(C):
    Grid=np.array([[0 for i in range(N+2)] for j in range(N+2)])
    for i in range(N+2):
        for j in range(N+2):
            for k in range(NPopu):
                if C[i,j][k]==1:
                    Grid[i,j]=k+1
    return Grid
Grid=convert(C)

def NumberNeighbors(i, j): #retourne le nombre de voisins de chaque population
    # assert(1<=i<=N and 1<=j<=N):'message'
    return [C[i + 1, j][k] + C[i + 1, j + 1][k] + C[i + 1, j - 1][k] + C[i - 1, j][k] + C[i - 1, j + 1][k] + C[i - 1, j - 1][k] + C[
        i, j + 1][k] + C[i, j - 1][k] for k in range (NPopu)]


def DeathCondition(i, j):  # la cellule meurt si elle a plus de x voisins ou moins de y voisins
    if sum(NumberNeighbors(i, j)[k] for k in range(NPopu)) > x or sum(NumberNeighbors(i, j)[k] for k in range(NPopu)) <= y:
        return True
    else:
        return False


def RebornCondition(i, j):  # la cellule nait si elle a z voisins
    if sum(NumberNeighbors(i, j)[k] for k in range(NPopu)) == z:
        return True
    else:
        return False


def update(t):
    global C
    a  = deepcopy(C)
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if DeathCondition(i, j):
                a[i, j] = [0 for k in range(NPopu)]
            if RebornCondition(i, j): #la cellule renait et prend la couleur majoritaire de ses voisins ( dans le cas z=3 si 2 voisins bleu clair et 1 voisin bleu foncé elle devient bleu clair)
                l=np.argmax(NumberNeighbors(i,j))
                a[i, j][l] = 1
    print(a)
    C =a
    Grid=convert(C)
    im.set_array(Grid)


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
im = plt.imshow(Grid, interpolation="none", cmap="Blues")

title = plt.title("")


ani = matplotlib.animation.FuncAnimation(fig, func=update,
                                         repeat=False, interval=100)
plt.show()