#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import log

def calculateUncertaintyEntropyBased(classiefierlabelandprobability):
    prob = classiefierlabelandprobability[1:]
    sum = 0
    for classprobability in prob:
        sum -= classprobability * log(2, classprobability)
    return sum

def calculateUncertaintyLeastConfident(classiefierlabelandprobability):
    return '0'

def calculateUncertaintyMarginSampling(classiefierlabelandprobability):
    return '0'

def calculateUncertaintyCouncilBasedVoteEntropy(classiefierlabelandprobability):
    return '0'

def calculateUncertaintyCouncilBasedKLDivergence(classiefierlabelandprobability):
    return '0'