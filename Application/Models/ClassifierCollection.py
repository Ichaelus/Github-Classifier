#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ClassifierCollection:
    """A class to deal with multiple Classification Modules"""
    
    classificationmodules = []
    #def __init__(self):
        # We need to test here later what´s the most recently used and safed collection and load it
        #self.classificationmodules = ...
    
    @classmethod
    def getClassificationModules(self):
        """Return some basic informations about each Classification Module."""
        return 'NotImplemented'
    @classmethod
    def getClassificationModule(self):
        return 'NotImplemented'
        
    @classmethod
    def addClassificationModule(self, module):
        """Add a classification module to the collection."""
        self.classificationmodules.append(module)

    @classmethod
    def removeClassificationModule(self, module):
        """Remove a classification module from the collection."""
        self.classificationmodules.remove(module)

    @classmethod
    def doLiveClassificationStep(self, sample):
        """Returns the sample with the label each classification module would assign """
        return 'NotImplemented'
    
    @classmethod
    def doLiveClassificationStepDetailled(self, sample):
        """Returns the sample with the probability each classification module would give each class"""
        return 'NotImplemented'
    
    @classmethod
    def StartLiveClassification(self, samples):
        """Each classification module starts labeling until finished or paused"""
        #da pauseable brauchen wir an der Stelle hier Threads
        return 'NotImplemented'
    
    @classmethod
    def PoolBasedActiveLearningGetQuery(self, anzahlclassificationrequests):
        """Calculates the best query to be answered by user"""
        return 'NotImplemented'

    @classmethod
    def StreamBasedActiveLearningGetIsSampleImportant(self, sample):
        """Calculates if the sample is someworth worth asking the user about"""
        return 'NotImplemented'

    @classmethod
    def TrainAllClassificationModules(self, data):
        """Trains all classification modules with the data, e.g. the newly labeled sample"""
        return 'NotImplemented'
    

    
