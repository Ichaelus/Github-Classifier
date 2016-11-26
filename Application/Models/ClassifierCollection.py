#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ClassificationModules.ClassificationModule
import DatabaseCommunication as DC
import ClassificationModules.ActiveLearningSpecific as AL

class ClassifierCollection:
    """A class to deal with multiple Classification Modules"""
    
    classificationmodules = []
    poolbasedalclassifierturn = 0


    def __init__(self):
        # Manually add each classification module we´re currently using
        self.classificationmodules = []
    
    @classmethod
    def getAllClassificationModules(self):
        """Return some basic informations about each Classification Module."""
        return self.classificationmodules

    @classmethod
    def SaveAllClassificationModules(self, stillundefined):
        """Saves all classification modules"""
        for classifier in self.classificationmodules:
		    classifier.SaveModule()

    @classmethod
    def getClassificationModule(self, classifiername):
        """Return the actual Classification Module object to do stuff like safing and loading."""
        for c in self.classificationmodules:
            if c.getName() == classifiername:
                return c
            else: 
                raise NameError('No classifier with this name')
        
    @classmethod
    def addClassificationModule(self, classificationmoduleobject):
        """Add a classification module to the collection. Der Name davon muss unique sein.
        Sollte nur am Anfang vom Programm verwendet werden"""
        #classificationModule-Namen müssen unique sein
        if any([c for c in self.classificationmodules if c.getName() == classificationmoduleobject.getName()]):
            raise NameError('Name must be unique')
        else :
            self.classificationmodules.append(classificationmoduleobject)

    @classmethod
    def removeClassificationModule(self, classifiername):
        """Remove a classification module from the collection."""
        self.classificationmodules.remove(self.getClassificationModule(classifiername))
    
    @classmethod
    def doStreamBasedALRound(self, formula, semisupervised=False, traininstantly=False, threshold = 0.5):
        """Ein zufälliges unlabeled Sample wird genommen, von jedem klassifiziert, und wenn sich 
        mindestens 1er unsicher ist, wird beim Benutzer nachgefragt"""
        sample = DC.getUnlabeledSingleSample()
        results = []
        unsure = False
        for c in self.classificationmodules:
            if not c.isMuteClassificationModule():
                resultc = c.predictLabelAndProbability(sample)
                uncertainty = 0.0
                if(formula == 'Entropy-Based'):
                    uncertainty = AL.calculateUncertaintyEntropyBased(resultc)
                elif(formula == "Least Confident"):
                    uncertainty = AL.calculateUncertaintyLeastConfident(resultc)
                elif(formula == "Margin-Sampling"):
                    uncertainty = AL.calculateUncertaintyMarginSampling(resultc)
                if(uncertainty > threshold):
                    unsure = True
                results.append(resultc, uncertainty)
        return (unsure, results)
    
    @classmethod
    def poolBasedALRound(self, formula, semisupervised=False, traininstantly=False):
        """Calculates the best query to be answered by user. First unmuted classifier 1
        gets to ask a question the next time this function is run, then unmuted classifier 2 etc."""
        data = DC.getUnlabeledData()
        #calculate which classifiers arent muted and which turn it is
        i = 0
        userquery = None
        for j in xrange(0, len(self.classificationmodules)):
            if(j == self.poolbasedalclassifierturn + i):
                c = self.classificationmodules[j]
                if not c.isMuteClassificationModule(): 
                    userquery = c.calculatePoolBasedQuery(formula, data)
                else:
                    i = i + 1
                    if (j == len(self.classificationmodules) and userquery == None):
                    # bevor er wenn gar kein Classifier nicht gemutet ist in endlosschleife hängen bleibt
                    # nochmal kontrollieren vorm zurückspringen zum anfang
                        if any([c for c in self.classificationmodules if not c.isMuteClassificationModule()]):
                            self.poolbasedalclassifierturn = 0
                            return self.poolBasedALRound(formula, semisupervised, traininstantly)
                        else: raise Exception('Error, trying to do poolBasedALRound without a non-muted classifier')
        return userquery

    @classmethod
    def TestAllClassificationModules(self):
        """Tests all classification modules, these do that by themselves and return results to this function"""
        data = DC.getTestData()
        results = []
        for c in self.classificationmodules:
            results.append(c.test(data))
        return results

    @classmethod
    def PredictSingleSample(self, repolink):
        """Returns the sample with the probability and label each classification module would assign"""
        data = DC.getFeatureVectorForRepo(repolink)
        results = []
        for c in self.classificationmodules:
            results.append(c.predictProbability(data))
        return results

    @classmethod
    def TrainAllClassificationModulesOnSample(self, repo):
        """Trains all classification modules with the data, e.g. the newly labeled sample"""
        results = []
        for c in self.classificationmodules:
            results.append(c.trainOnSample(repo))
        return results
    

    
