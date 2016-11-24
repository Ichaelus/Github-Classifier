#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from ClassificationModule import ClassificationModule

class EnsembleClassifier(ClassificationModule):

    __metaclass__  = ABCMeta
    subclassifiers = []

    @abstractmethod
    def getSubClassifierNames(self):
        pass

    @abstractmethod
    def getSubClassifierDescription(self):
        pass



    