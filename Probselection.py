import math
import numpy as np


def Probtarget(rand, problist):
    tgt = 0
    listlen = len(problist)
    probsum = sum(problist)
    if probsum == 0:
        tgt = -1
    else:
        culprob = [0.0 for i in range(listlen)]
        for i in range(listlen):
            if i == 0:
                culprob[i] = 1.0 * problist[i] / probsum
            else:
                culprob[i] = culprob[i - 1] + 1.0 * problist[i] / probsum
        left = 0
        right = listlen - 1
        if rand <= culprob[0]:
            tgt = 0
        else:
            while (right - left) > 1:
                middle = math.floor((left + right) / 2)
                middle = int(middle)
                if rand <= culprob[middle]:
                    right = middle
                else:
                    left = middle
            tgt = right

    return tgt

def Probneigh(rand, allproblist, neighlist):
    tgt = 0
    listlen = len(neighlist)
    problist = np.zeros(listlen)
    tempindex = 0
    for i in neighlist:
        problist[tempindex] = allproblist[i]
        tempindex += 1

    probsum = sum(problist)
    if probsum == 0:
        tgt = max(problist)
        tgtid = np.where(problist == tgt)
        tgtid = tgtid[0][0]
        tgt = neighlist[tgtid]
    else:
        culprob = [0.0 for i in range(listlen)]
        for i in range(listlen):
            if i == 0:
                culprob[i] = 1.0 * problist[i] / probsum
            else:
                culprob[i] = culprob[i - 1] + 1.0 * problist[i] / probsum
        left = 0
        right = listlen - 1
        if rand <= culprob[0]:
            tgt = 0
        else:
            while (right - left) > 1:
                middle = math.floor((left + right) / 2)
                middle = int(middle)
                if rand <= culprob[middle]:
                    right = middle
                else:
                    left = middle
            tgt = right
        tgt = neighlist[tgt]
    return tgt
