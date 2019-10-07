import sys
import numpy as np
import random
from igraph import *

count = 0

def Adjacency2Graph(N, network):
    g = Graph()
    g.add_vertices(N)

    for i in range(N):
        for j in range(i):
            if network[i][j]:
                g.add_edges([(i, j)])

    global count
    if count == 0:
        g.vs['label'] = [i for i in range(N)]
    count += 1
    return g

def randranking(N, network, n):
    topn = np.zeros(n)

    randarr = list(range(N))
    random.shuffle(randarr)
    for i in range(n):
        topn[i] = randarr[i]

    return topn


def degranking(N, network, n):
    degree = np.zeros([N, 2])

    for i in range(N):
        degree[i][0] = np.sum(network[i])
        degree[i][1] = i

    newdegree = tuple(degree)

    tempdegree = sorted(newdegree, key=lambda x: x[0], reverse=True)

    topn = np.zeros(n)

    for i in range(n):
        topn[i] = tempdegree[i][1]

    return topn


def statedegranking(N, network, n, a, b):
    topn = np.zeros(n)
    state = np.zeros(N)
    neighstate = np.zeros([N, N])
    for i in range(N):
        for j in range(N):
            if network[i][j] == 1:
                if state[j] == 0:
                    neighstate[i][j] = a
                else:
                    neighstate[i][j] = b

    r = 0
    while r < n:
        templist = list(topn[0:r])
        degree = np.zeros([N - r, 2])

        k = 0
        for i in range(N):
            if i not in templist:
                degree[k][0] = np.sum(neighstate[i])
                degree[k][1] = i
                k += 1

        newdegree = tuple(degree)

        tempdegree = sorted(newdegree, key=lambda x: x[0], reverse=True)

        topn[r] = tempdegree[0][1]
        i = int(topn[r])
        state[i] = 1

        for j in range(N):
            if network[j][i] == 1:
                neighstate[j][i] = b

        r += 1

    return topn

def discountranking(N, network, n, a):
    topn = np.zeros(n)
    state = np.zeros(N)
    neighstate = np.zeros([N, N])
    for i in range(N):
        for j in range(N):
            if network[i][j] == 1:
                neighstate[i][j] = 1

    r = 0
    while r < n:
        templist = list(topn[0:r])
        degree = np.zeros([N - r, 2])

        k = 0
        for i in range(N):
            if i not in templist:
                degree[k][0] = np.sum(neighstate[i])
                degree[k][1] = i
                k += 1

        newdegree = tuple(degree)

        tempdegree = sorted(newdegree, key=lambda x: x[0], reverse=True)

        topn[r] = tempdegree[0][1]
        i = int(topn[r])
        state[i] = 3

        for j in range(N):
            if network[i][j] == 1:
                if state[j] == 0 or state[j]==1:
                    state[j] = 2
                for k in range(N):
                    if network[j][k] == 1 and network[i][k]==0:
                        if state[k] == 0:
                            state[k] = 1

        neighstate = np.zeros([N, N])
        for j in range(N):
            for k in range(N):
                if network[j][k] == 1:
                    if state[k] == 0:
                        neighstate[j][k] = 1
                    if state[k] == 1:
                        neighstate[j][k] = 1-a*a
                    if state[k] == 2:
                        neighstate[j][k] = 1-a
                    if state[k] == 3:
                        neighstate[j][k] = 0

        r += 1

    return topn

def negweightedranking(N, network, n, a):

    topn = np.zeros(n)
    state = np.zeros(N)
    seedneigh = np.zeros(N)
    neighstate = np.zeros([N,N])
    for i in range(N):
        for j in range(N):
            if network[i][j] == 1:
                neighstate[i][j] = 1

    r = 0
    while r<n:
        templist = list(topn[0:r])
        degree = np.zeros([N-r,2])

        k = 0
        for i in range(N):
            if i not in templist:
                degree[k][0] = np.sum(neighstate[i])
                degree[k][1] = i
                k += 1

        newdegree = tuple(degree)

        tempdegree = sorted(newdegree, key= lambda x: x[0], reverse = True)

        topn[r] = tempdegree[0][1]
        i = int(topn[r])
        state[i] = 1

        for j in range(N):
            if network[i][j] == 1 and state[j] == 1:
                seedneigh[i] += 1
                seedneigh[j] += 1

        neighstate = np.zeros([N,N])
        for j in range(N):
            for k in range(N):
                if network[j][k] == 1:
                    if state[k] == 0:
                        neighstate[j][k] = 1

                    if state[k] == 1:
                        neighstate[j][k] = -1-a*seedneigh[k]

        r += 1

    # cleardeg = np.zeros(N)
    # for i in range(N):
    #     for j in range(N):
    #         if state[j] == 0 and network[i][j] == 1:
    #             cleardeg[i] += 1
    # X = 0
    # for i in range(n):
    #     j = int(topn[i])
    #     X+=cleardeg[j]
    # print(X)
    # input()

    return topn

def posweightedranking(N, network, n, a):

    topn = np.zeros(n)
    state = np.zeros(N)
    seedneigh = np.zeros(N)
    neighstate = np.zeros([N,N])
    for i in range(N):
        for j in range(N):
            if network[i][j] == 1:
                neighstate[i][j] = 1

    r = 0
    while r<n:
        templist = list(topn[0:r])
        degree = np.zeros([N-r,2])

        k = 0
        for i in range(N):
            if i not in templist:
                degree[k][0] = np.sum(neighstate[i])
                degree[k][1] = i
                k += 1

        newdegree = tuple(degree)

        tempdegree = sorted(newdegree, key= lambda x: x[0], reverse = True)

        topn[r] = tempdegree[0][1]
        i = int(topn[r])
        state[i] = 1

        for j in range(N):
            if network[i][j] == 1 and state[j] == 1:
                seedneigh[i] += 1
                seedneigh[j] += 1

        neighstate = np.zeros([N,N])
        for j in range(N):
            for k in range(N):
                if network[j][k] == 1:
                    if state[k] == 0:
                        neighstate[j][k] = 1

                    if state[k] == 1:
                        neighstate[j][k] = 1+a*seedneigh[k]

        r += 1

    # cleardeg = np.zeros(N)
    # for i in range(N):
    #     for j in range(N):
    #         if state[j] == 0 and network[i][j] == 1:
    #             cleardeg[i] += 1
    # X = 0
    # for i in range(n):
    #     j = int(topn[i])
    #     X+=cleardeg[j]
    # print(X)
    # input()

    return topn

def BetweenNessRanking(N, network, n):
    topn = np.zeros(n)
    g = Adjacency2Graph(N, network)
    BetweenNessList = g.betweenness()
    BetweenNessArray = np.array(BetweenNessList)
    BetweenNessSort = BetweenNessArray.argsort()[::-1]

    topn = BetweenNessSort[0:n]
    return topn


def KCoreRanking(N, network, n):
    topn = np.zeros(n)
    g = Adjacency2Graph(N, network)
    KCoreList = []
    CoreNum = 1
    ResNodeNum = N
    OriginalNum = [i for i in range(N)]
    while ResNodeNum > 0:
        while True:
            deleteList = []
            for i in range(ResNodeNum):
                if g.degree(i) <= CoreNum:
                    KCoreList += [OriginalNum[i]]
                    deleteList += [i]
            OriginalNum = [OriginalNum[i] for i in range(len(OriginalNum)) if i not in deleteList]

            g.delete_vertices(deleteList)
            ResNodeNum -= len(deleteList)
            if not len(deleteList):
                break
        CoreNum += 1
    KCoreList.reverse()
    KCoreArray = np.array(KCoreList)
    topn = KCoreArray[0:n]

    #print(KCoreArray)
    return topn

def position(N, Invaderlist, Neigh, network):

    pos = np.zeros(3)

    n = len(Invaderlist)

    deg = np.zeros(n)

    for i in Invaderlist:
        deg[i] = len(Neigh[i])

    avedeg = np.mean(deg)

    dist = np.zeros(n)

    for i in Invaderlist:
        disti = np.zeros(N)
        for j in range(N):
            if i==j:
                disti[j]=0
            if i!=j:
                if network[i][j]==1:
                    disti[j] = 1
                else:
                    disti[j] = N
        flag = ['False']*N
        flag[i] = True
        minv = i

        for j in range(N):
            for k in Neigh(minv):
                if disti[minv] + network[minv][k] < disti[k]:
                    disti[k] = disti[minv] + network[minv][k]

            minvalue = N+1
            for k in range(N):
                if flag[k] == False:
                    if disti[k] < minvalue:
                        minvalue = disti[k]
                        minv = k
            flag[minv] = True

        for j in Invaderlist:
            dist[i] += disti[j]

    if n >1:
        dist /= (n-1)

    avedist = np.mean(dist)

    coversize = 0
    state = np.zeros(N)
    for i in Invaderlist:
        state[i] = 1
        for j in Neigh(i):
            state[j] = 1
    coversize = sum(state)

    pos[0] = avedeg
    pos[1] = avedist
    pos[2] = coversize

    return pos
