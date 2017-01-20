#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import log

def calculateUncertaintyEntropyBased(classifierlabelandprobability):
    prob = classifierlabelandprobability[1:]
    sum = 0
    for classprobability in prob:
        if(classprobability > 0):
            sum -= classprobability * log(classprobability, 2)
    return sum

def calculateUncertaintyLeastConfident(classifierlabelandprobability):
    return 1 - classifierlabelandprobability[classifierlabelandprobability[0]+1]

def calculateUncertaintyMarginSampling(classifierlabelandprobability):
    prob = classifierlabelandprobability[1:]
    best = prob[classifierlabelandprobability[0]]
    second = 0
    for p in prob:
        if p < best and p > second:
            second = p
    return best - second
    