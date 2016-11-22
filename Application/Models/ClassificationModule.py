#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class ClassificationModule:
    __metaclass__ = ABCMeta

    description = "Doesnt have a description yet"
    muted = False
    
    @classmethod
    def getDescription(self):
        return self.description
    
    @classmethod
    def calculateUncertainty(self):
        return self.description
    
    @classmethod 
    def safeStatus(self):
        return 'NotImplemented'

    @classmethod 
    def loadStatus(self):
        return 'NotImplemented'
    
    @abstractmethod
    def resetAllTraining(self):
        """Reset classification module to status before training"""
        pass

    @abstractmethod
    def trainOnSample(self, sample):
        """Trainiere (inkrementell) mit Sample. Evtl zusätzlich mit best. Menge alter Daten, damit overfitten auf neue Daten verhindert wird."""
        pass

    @abstractmethod
    def train(self, samples, classes):
        """Trainiere mit Liste von Daten. Evtl weitere Paramter nötig (nb_epoch, learning_rate, ...)"""
        pass

    @abstractmethod
    def predictLabel(self, sample):
        """Gibt zurück, wie der Klassifikator ein gegebenes Sample klassifizieren würde"""
        pass
    
    @abstractmethod
    def detailledPrediction(self, sample):
        """Return the probability the module assignes each label"""
        pass

    @abstractmethod
    def formatInputData(self):
        pass

    @classmethod
    def muteClassificationModule(self):
        """The Module loses it´s right to give queries to the user"""
        self.muted = True

    @classmethod
    def unmuteClassificationModule(self):
        """The Module gains the right back to give queries to the user"""
        self.muted = False

    @classmethod
    def isMuteClassificationModule(self):
        """Returns if the module is muted or not"""
        return self.muted


    