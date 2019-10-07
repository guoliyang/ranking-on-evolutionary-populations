import sys
import numpy as np
import copy

from Network import *
from Probselection import *
from Ranking import *

N = 200
E = 400


R = 1
S =  -1+int(sys.argv[1])*0.2
T =  int(sys.argv[2])*0.2
P = 0
w = int(sys.argv[3])*0.01

Round = 200

r = 0

Invadersize = int(sys.argv[6])*20

networktype = int(sys.argv[4])
rankingtype = int(sys.argv[5])


Transition = [0] * Round
Maxsize = [0] * Round
Duration = [0] * Round

while r < Round:

    state = [0] * N
    payoff = [0.0] * N
    prosperity = [0.0] * N

    if networktype==1:
        network = latticegen(N, 10, 20)
    if networktype==2:
        network = randomgen(N, E)
    if networktype==3:
        network = scalefreegen(N, 5)
    if networktype==4:
        network = smallworldgen(N, 0.2)

    Neigh = [[] for i in range(N)]
    for i in range(N):
        for j in range(N):
            if network[i][j] == 1:
                Neigh[i].append(j)

    Pi = [[R, S], [T, P]]

    for i in range(N):
        for j in Neigh[i]:
            payoff[i] = payoff[i] + Pi[state[i]][state[j]]
        prosperity[i] = 1-w+w*payoff[i]

    transition = False
    recovery = False
    activelinknum = 0

    t = 0
    maxsize = 1

    Invaderlist = np.zeros(Invadersize)

    #print("Starting======, the round of ", str(r))

    while transition == False and recovery == False:
        t = t + 1

        #print(t,sum(state))

        if t == 1:
            if rankingtype == 1:
                Invaderlist =randranking(N, network, Invadersize)
            if rankingtype == 2:
                Invaderlist =degranking(N, network, Invadersize)
            if rankingtype == 3:
                Invaderlist =BetweenNessRanking(N, network, Invadersize)
            if rankingtype == 4:
                Invaderlist =KCoreRanking(N, network, Invadersize)
            if rankingtype == 5:
                Invaderlist =discountranking(N, network, Invadersize, 0.5)
            if rankingtype == 6:
                Invaderlist =negweightedranking(N, network, Invadersize, 0.1)
            if rankingtype == 7:
                Invaderlist =posweightedranking(N, network, Invadersize, 0.1)

            for i in range(len(Invaderlist)):
                j = int(Invaderlist[i])
                state[j] = 1 - state[j]

            for j in Invaderlist:
            	j = int(j)
            	for k in Neigh[j]:
            		if state[k]!=state[j]:
            			activelinknum += 1

        if maxsize < sum(state):
            maxsize = sum(state)

        # remover
        i = np.random.randint(0, N)
        while len(Neigh[i])==0:
            i = np.random.randint(0, N)

        # reproducer
        rand = np.random.rand(1)
        j = Probneigh(rand, prosperity,Neigh[i])

        if state[i] != state[j]:
            tempstate = state[i]
            state[i] = state[j]
            payoff[i] = 0
            for k in Neigh[i]:
                payoff[k] = payoff[k]-Pi[state[k]][tempstate] + Pi[state[k]][state[i]]
                prosperity[k] = 1-w+w*payoff[k]
                payoff[i] += Pi[state[i]][state[k]]
            prosperity[i] = 1-w+w*payoff[i]

            for k in Neigh[i]:
                if state[k] == state[i]:
                    activelinknum -= 1
                else:
                    activelinknum += 1


        if maxsize < sum(state):
            maxsize = sum(state)

        if sum(state) == N:
            transition = True
            Transition[r] = 1
            Maxsize[r] = maxsize
            Duration[r] = t

        if sum(state) == 0:
            recovery = True
            Transition[r] = 0
            Maxsize[r] = maxsize
            Duration[r] = t

        if activelinknum == 0:
            if sum(state)>N/2:
                transition = True
                Transition[r] = 1
                Maxsize[r] = maxsize
                Duration[r] = t
            else:
                recovery = True
                Transition[r] = 0
                Maxsize[r] = maxsize
                Duration[r] = t

    print(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6],Transition[r], Maxsize[r], Duration[r])

    filename = 'Output' + str(sys.argv[1]) + "and" + str(sys.argv[2])+"and" + str(sys.argv[3])+ "and" + str(sys.argv[4] )+"and" + str(sys.argv[5])+"and" + str(sys.argv[6])
    f = open(filename, 'a')
    f.write(str(Transition[r]) + '\t' + str(Maxsize[r]) + '\t' + str(Duration[r]) + '\n')
    f.close()

    r = r + 1
