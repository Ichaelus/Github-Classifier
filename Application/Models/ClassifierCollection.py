#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ClassifierCollection:
    """A class to deal with multiple Classification Modules"""
    
    classificationmodules = []

    def __init__(self):
        # Manually add each classification module we´re currently using
        self.classificationmodules = []
    
    @classmethod
    def getAllClassificationModules(self):
        """Return some basic informations about each Classification Module."""
        return 'NotImplemented'

    @classmethod
    def SaveAllClassificationModules(self, stillundefined):
        """Saves all classification modules"""
		#for i in classificationmodules:
		#	i.SaveModule()
        return 'NotImplemented'

    @classmethod
    def getClassificationModule(self, classifiername):
        """Return the actual Classification Module object to do stuff like safing and loading."""
        return 'NotImplemented'
        
    @classmethod
    def addClassificationModule(self, classificationmoduleobject):
        """Add a classification module to the collection."""
        #classificationModule-Namen müssen unique sein
        if any([c for c in self.classificationmodules if c.getName() == classificationmoduleobject.getName()]):
            self.classificationmodules.append(classificationmoduleobject)
        else :
            raise NameError('Name must be unique')

    @classmethod
    def removeClassificationModule(self, classifiername):
        """Remove a classification module from the collection."""
        self.classificationmodules.remove(self.getClassificationModule(classifiername))
    
    @classmethod
    def DoStreamBasedALRound(self, formula, semisupervised=False, traininstantly=False):
        """Each classification module starts labeling until finished or paused"""
        #da pauseable brauchen wir an der Stelle hier Threads
        return 'NotImplemented'
    
    @classmethod
    def PoolBasedALRound(self, formula, semisupervised=False, traininstantly=False):
        """Calculates the best query to be answered by user. First unmuted classifier 1
        gets to ask a question, then unmuted classifier 2 etc."""
        return 'NotImplemented'

    @classmethod
    def TestAllClassificationModules(self):
        """Tests all classification modules, these do that by themselfes and return results to this function"""
        return 'NotImplemented'

    @classmethod
    def PredictSingleSample(self, repolink):
        """Returns the sample with the probability and label each classification module would assign"""
        return 'NotImplemented'

    @classmethod
    def TrainAllClassificationModules(self, stillundefined):
        """Trains all classification modules with the data, e.g. the newly labeled sample"""
        return 'NotImplemented'
    

    
