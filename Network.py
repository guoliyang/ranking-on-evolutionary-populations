import sys
import numpy as np
from Probselection import Probtarget


def randomgen(N, E):
    Edgelist = []
    for i in range(0, N):
        for j in range(0, i):
            Edgelist.append([i, j])

    np.random.shuffle(Edgelist)

    network = np.zeros((N, N))
    for i in range(0, E):

        a = Edgelist[i][0]
        b = Edgelist[i][1]
        network[a][b] = 1
        network[b][a] = 1
    return network


def latticegen(N,m,n):

    network = np.zeros((N, N))
    for i in range(m):
        for j in range(n):
            x = i*n+j

            if i == 0:
                if j == 0:
                    y1 = i*n+j+1
                    y2 = (i+1)*n + j
                    network[x][y1] = 1
                    network[y1][x] = 1
                    network[x][y2] = 1
                    network[y2][x] = 1
                elif j==n-1:
                    y1 = i*n+j-1
                    y2 = (i+1)*n + j
                    network[x][y1] = 1
                    network[y1][x] = 1
                    network[x][y2] = 1
                    network[y2][x] = 1
                else:
                    y1 = i*n+j-1
                    y2 = i*n+j+1
                    y3 = (i+1)*n + j
                    network[x][y1] = 1
                    network[y1][x] = 1
                    network[x][y2] = 1
                    network[y2][x] = 1
                    network[x][y3] = 1
                    network[y3][x] = 1
            elif i == m-1:
                if j == 0:
                    y1 = i*n+j+1
                    y2 = (i-1)*n + j
                    network[x][y1] = 1
                    network[y1][x] = 1
                    network[x][y2] = 1
                    network[y2][x] = 1
                elif j==n-1:
                    y1 = i*n+j-1
                    y2 = (i-1)*n + j
                    network[x][y1] = 1
                    network[y1][x] = 1
                    network[x][y2] = 1
                    network[y2][x] = 1
                else:
                    y1 = i*n+j-1
                    y2 = i*n+j+1
                    y3 = (i-1)*n + j
                    network[x][y1] = 1
                    network[y1][x] = 1
                    network[x][y2] = 1
                    network[y2][x] = 1
                    network[x][y3] = 1
                    network[y3][x] = 1
            else:
                if j == 0:
                    y1 = i*n+j+1
                    y2 = (i-1)*n + j
                    y3 = (i+1)*n + j
                    network[x][y1] = 1
                    network[y1][x] = 1
                    network[x][y2] = 1
                    network[y2][x] = 1
                    network[x][y3] = 1
                    network[y3][x] = 1
                elif j==n-1:
                    y1 = i*n+j-1
                    y2 = (i-1)*n + j
                    y3 = (i+1)*n + j
                    network[x][y1] = 1
                    network[y1][x] = 1
                    network[x][y2] = 1
                    network[y2][x] = 1
                    network[x][y3] = 1
                    network[y3][x] = 1
                else:
                    y1 = i*n+j-1
                    y2 = i*n+j+1
                    y3 = (i-1)*n + j
                    y4 = (i+1)*n + j
                    network[x][y1] = 1
                    network[y1][x] = 1
                    network[x][y2] = 1
                    network[y2][x] = 1
                    network[x][y3] = 1
                    network[y3][x] = 1
                    network[x][y4] = 1
                    network[y4][x] = 1

    return network

def smallworldgen(N,p):
    network = np.zeros((N, N))
    for i in range(N):
        x = (N+i+1)%N
        rand = np.random.rand(1)
        if rand < p:
            x = np.random.randint(0, N)
            while x==i:
                x = np.random.randint(0, N)
        network[i][x] = 1
        network[x][i] = 1

        x = (N+i+2)%N
        rand = np.random.rand(1)
        if rand < p:
            x = np.random.randint(0, N)
            while x==i:
                x = np.random.randint(0, N)
        network[i][x] = 1
        network[x][i] = 1

    return network

def scalefreegen(N,n):
    deg = np.zeros(N)
    network = np.zeros((N, N))
    for i in range(n):
        for j in range(i+1,n):
            network[i][j] = 1
            network[j][i] = 1
            deg[i] += 1
            deg[j] += 1

    for i in range(n,N):
        rand = np.random.rand(1)
        j = Probtarget(rand, deg)
        rand = np.random.rand(1)
        k = Probtarget(rand, deg)
        while k == j:
            rand = np.random.rand(1)
            k = Probtarget(rand, deg)
        network[i][j] = 1
        network[j][i] = 1
        deg[i] += 1
        deg[j] += 1
        network[i][k] = 1
        network[k][i] = 1
        deg[i] += 1
        deg[k] += 1

    return network
