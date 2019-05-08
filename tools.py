# Ce fichier regroupe les différents outils utilisés : génération, quantification et analyse des expériences.

import numpy as np
from scipy.optimize import leastsq
from xlrd import open_workbook
import matplotlib.pyplot as plt

# GENERATION
def randomGrid(N, pop):
    return np.random.choice([0, 1], size=(N, N), p=[1-pop, pop])


# QUANTIFICATION
def count(C):
    N = len(C)-2
    count = 0
    for i in range(1, N+1):
        for j in range(1, N+1):
            if C[i][j] != 0:
                count += 1
    return count


def meanAge(C):
    N = len(C)-2
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


def openEx(name,sheetIndex,columnIndex,columnSize):
    book = open_workbook(name)
    sheet = book.sheet_by_index(sheetIndex)
    column = []

    for row in range(1, columnSize+1): #start from 1, to leave out row 0
        column.append(sheet.cell(row, columnIndex).value)

    return column

def PLresidual(vars, x, data, eps_data):
    sc = vars[0]
    beta = vars[1]
    amp = vars[2]

    n = len(x)
    model = np.zeros(n)
    for i in range(n):
        model[i] = amp * (sc-x[i])**beta

    res = np.zeros(n)
    for i in range(n):
        res[i] = (data[i]-model[i]) / eps_data

    return res
