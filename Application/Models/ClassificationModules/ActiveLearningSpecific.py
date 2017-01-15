#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import log

def calculateUncertaintyEntropyBased(classiefierlabelandprobability):
    prob = classiefierlabelandprobability[1:]
    sum = 0
    for classprobability in prob:
        if(classprobability > 0):
            sum -= classprobability * log(classprobability, 2)
    return sum

def calculateUncertaintyLeastConfident(classiefierlabelandprobability):
    return 1 - classiefierlabelandprobability[classiefierlabelandprobability[0]+1]

def calculateUncertaintyMarginSampling(classiefierlabelandprobability):
    prob = classiefierlabelandprobability[1:]
    best = prob[classiefierlabelandprobability[0]]
    second = 0
    for p in prob:
        if p < best and p > second:
            second = p
    return best - second

def calculateUncertaintyCouncilBasedVoteEntropy(classiefierlabelandprobability):
    return '0'

def calculateUncertaintyCouncilBasedKLDivergence(classiefierlabelandprobability):
    return '0'