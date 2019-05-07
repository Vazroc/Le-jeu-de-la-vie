# Fichier principal à éxécuter. Contient le cas d'une population simple, avec un taux de synchronisation donné.

import random
from copy import deepcopy
import matplotlib.animation
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
import xlwt
from tempfile import TemporaryFile
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


# VARIATION OF POPULATION RATE
def main2():
    p = 25
    popList = np.linspace(0,1,p)
    syncList = [0.1,0.3,0.5,0.75,0.9,0.95,1]
    nsteps = 150

    book = xlwt.Workbook()
    sheet1 = book.add_sheet('Activity')
    sheet2 = book.add_sheet('Density')
    sheet3 = book.add_sheet('Mean age')
    for i,e in enumerate(popList*100):
        sheet1.write(i,0,e)
        sheet2.write(i,0,e)
        sheet3.write(i,0,e)
    j = 0
    for sync in syncList: # synchronisation rate : 0 = completely asynchronous (no updating) -> 1 = completely synchronous (basic simultaneous updating)
        j += 1
        print("main2")
        activityRes = np.zeros(p)
        densityRes = np.zeros(p)
        ageRes = np.zeros(p)
        for i in range(p):
            print("i =", i)
            # Grid & initial situation
            N = 100  # Dimension du 2D array, sans compter les bordures
            pop = popList[i] # proportion of living cells at the beginning

            C = np.zeros((N + 2, N + 2))  # le 2D array. 0: pas de cellule.1: cellule présente.
            C[1:N+1, 1:N+1] = randomGrid(N, pop)

            t = 0
            while t < nsteps:
                C = update(t, C, sync)[0]
                t += 1
            activityRes[i] = update(t, C, sync)[1]/N**2*100
            densityRes[i] = count(C)/N**2*100
            ageRes[i] = meanAge(C)

        x_new = np.linspace(0, 1, 100)*100
        plt.figure(1)
        spl = make_interp_spline(popList*100, activityRes, k=2) #BSpline object
        activity_smooth = spl(x_new)
        plt.plot(x_new, activity_smooth, label=str(sync))
        plt.figure(2)
        spl = make_interp_spline(popList*100, densityRes, k=2) #BSpline object
        density_smooth = spl(x_new)
        plt.plot(x_new, density_smooth, label=str(sync))
        plt.figure(3)
        spl = make_interp_spline(popList*100, ageRes, k=2) #BSpline object
        age_smooth = spl(x_new)
        plt.plot(x_new, age_smooth, label=str(sync))

        for i,e in enumerate(activityRes):
            sheet1.write(i,j,e)
        for i,e in enumerate(densityRes):
            sheet2.write(i,j,e)
        for i,e in enumerate(ageRes):
            sheet3.write(i,j,e)

    plt.figure(1)
    plt.title("Activity of cells after "+str(nsteps)+" steps against initial population rate")
    plt.ylabel("Activity of cells (%)")
    plt.xlabel("Initial population rate (%)")
    plt.xlim(0,100)
    plt.legend()
    plt.figure(2)
    plt.title("Density of living cells after "+str(nsteps)+" steps against initial population rate")
    plt.ylabel("Density of living cells (%)")
    plt.xlabel("Initial population rate (%)")
    plt.xlim(0,100)
    plt.legend()
    plt.figure(3)
    plt.title("Mean age of living cells after "+str(nsteps)+" steps against initial population rate")
    plt.ylabel("Mean age of living cells")
    plt.xlabel("Initial population rate (%)")
    plt.xlim(0,100)
    plt.legend()

    # Saving data
    name = "poprate.xls"
    book.save(name)
    book.save(TemporaryFile())

# VARIATION OF SYNCHRONISATION RATE
def main3():
    s = 25
    popList = [0.1,0.3,0.5,0.75,0.9,0.95,1]
    syncList = np.linspace(0,1,s)
    nsteps = 150

    book = xlwt.Workbook()
    sheet1 = book.add_sheet('Activity')
    sheet2 = book.add_sheet('Density')
    sheet3 = book.add_sheet('Mean age')
    for i,e in enumerate(syncList*100):
        sheet1.write(i,0,e)
        sheet2.write(i,0,e)
        sheet3.write(i,0,e)
    j = 0
    for pop in popList:
        j += 1
        print("main3")
        activityRes = np.zeros(s)
        densityRes = np.zeros(s)
        ageRes = np.zeros(s)
        for i in range(s):
            print("i =", i)
            # Grid & initial situation
            N = 100  # Dimension du 2D array, sans compter les bordures
            sync = syncList[i] # proportion of living cells at the beginning

            C = np.zeros((N + 2, N + 2))  # le 2D array. 0: pas de cellule.1: cellule présente.
            C[1:N+1, 1:N+1] = randomGrid(N, pop)

            t = 0
            while t < nsteps:
                C = update(t, C, sync)[0]
                t += 1
            activityRes[i] = update(t, C, sync)[1]/N**2*100
            densityRes[i] = count(C)/N**2*100
            ageRes[i] = meanAge(C)

        x_new = np.linspace(0, 1, 100)*100
        plt.figure(4)
        spl = make_interp_spline(syncList*100, activityRes, k=2) #BSpline object
        activity_smooth = spl(x_new)
        plt.plot(x_new, activity_smooth, label=str(pop))
        plt.figure(5)
        spl = make_interp_spline(syncList*100, densityRes, k=2) #BSpline object
        density_smooth = spl(x_new)
        plt.plot(x_new, density_smooth, label=str(pop))
        plt.figure(6)
        spl = make_interp_spline(syncList*100, ageRes, k=2) #BSpline object
        age_smooth = spl(x_new)
        plt.plot(x_new, age_smooth, label=str(pop))

        for i,e in enumerate(activityRes):
            sheet1.write(i,j,e)
        for i,e in enumerate(densityRes):
            sheet2.write(i,j,e)
        for i,e in enumerate(ageRes):
            sheet3.write(i,j,e)

    plt.figure(4)
    plt.title("Activity of cells after "+str(nsteps)+" steps against synchronisation rate")
    plt.ylabel("Activity of cells (%)")
    plt.xlabel("Synchronisation rate (%)")
    plt.xlim(10,100)
    plt.legend()
    plt.figure(5)
    plt.title("Density of living cells after "+str(nsteps)+" steps against synchronisation rate")
    plt.ylabel("Density of living cells (%)")
    plt.xlabel("Synchronisation rate (%)")
    plt.xlim(10,100)
    plt.legend()
    plt.figure(6)
    plt.title("Mean age of living cells after "+str(nsteps)+" steps against synchronisation rate")
    plt.ylabel("Mean age of living cells")
    plt.xlabel("Synchronisation rate (%)")
    plt.xlim(10,100)
    plt.legend()

    # Saving data
    name = "syncrate.xls"
    book.save(name)
    book.save(TemporaryFile())

# MAIN
main2()
main3()
plt.show()

