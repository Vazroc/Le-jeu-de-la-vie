# Ce fichier regroupe les différents outils utilisés : génération, quantification et analyse des expériences.

import numpy as np

# GENERATION
def randomGrid(N, pop):
    return np.random.choice([0, 1], size=(N, N), p=[pop, 1-pop])


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
