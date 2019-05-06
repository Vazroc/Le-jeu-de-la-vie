def count(C):
    count = 0
    for i in range(1, N+1):
        for j in range(1, N+1):
            if C[i][j] != 0:
                count += 1
    return count


def meanAge(C):
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
