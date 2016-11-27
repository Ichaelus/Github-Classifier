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
		    classifier.saveModule()

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

    #sollten wir nicht brauchen, da keine Funktion zum Entfernen von Classifiern aus der ClassifierCollection
    #von der GUI bereitgestellt wird, alle die in start hinzugefügt werden sind bis zum Ende dabei
    #eine Verwendung hiervon kann zu unvorhergesehenen Fehlern beim PoolBasedAL sorgen (auch wenn dies fixbar ist,
    #macht nur manches ein wenig umständlicher ohne dass wir dafür was nützliches bekommen)
    #@classmethod
    #def removeClassificationModule(self, classifiername):
    #    """Remove a classification module from the collection."""
    #    self.classificationmodules.remove(self.getClassificationModule(classifiername))
    
    @classmethod
    def doStreamBasedALRound(self, formula, semisupervised=False, thresholdunsupervisedl = 0.1, thresholdquery = 0.5):
        """Ein zufälliges unlabeled Sample wird genommen, von jedem klassifiziert, und wenn sich 
        mindestens 1er unsicher ist, wird beim Benutzer nachgefragt,
        ggf. wenn Unsicherheit niedrig genug wird es wenn semisupervised für Semi-Supervised Learning verwendet"""
        sample = DC.getUnlabeledSingleSample()
        results = []
        unsure = False
        SemiSupervisedL = False
        SemiSupervisedLabel = None
        for c in self.classificationmodules:
            if not c.isMuteClassificationModule():
                resultc = c.predictLabelAndProbability(sample)
                uncertainty = None
                if(formula == 'Entropy-Based'):
                    uncertainty = AL.calculateUncertaintyEntropyBased(resultc)
                elif(formula == "Least Confident"):
                    uncertainty = AL.calculateUncertaintyLeastConfident(resultc)
                elif(formula == "Margin-Sampling"):
                    uncertainty = AL.calculateUncertaintyMarginSampling(resultc)
                else: raise Exception("No such formula")
                if(uncertainty != None and uncertainty > thresholdquery):
                    unsure = True
                    DC.moveRepoFromUnlabeledToToClassify(sample)
                elif(uncertainty != None and uncertainty < thresholdunsupervisedl ): 
                    #Hier müssen wir uns noch Gedanken machen, vlt kontrollieren
                    #wir hier nochmal ob auch wirklich alle Classifier das selbe sagen und dann
                    #nehmen wir diese Vorhersage von allen als Label nur dann?
                    Label = NotImplemented
                    sampleNowWithLabel = NotImplemented
                    DC.moveRepoFromUnlabeledToSemiSupervised(sampleNowWithLabel)
                    SemiSupervisedLabel = Label
                    SemiSupervisedL = True
                results.append([resultc, uncertainty])
        return (sample, unsure, SemiSupervisedL, SemiSupervisedLabel, results)
    
    @classmethod
    def ALTrainInstantlyAllClassificationModules(self, sample):
        """Train all ClassificationModules with the user query result"""
        DC.moveRepoFromToClassifyToTrain(sample)
        for c in self.classificationmodules:
            c.trainOnSample(sample)
    
    @classmethod
    def doPoolBasedALRound(self, formula, semisupervised=False, traininstantly=False):
        """Calculates the best query to be answered by user. First unmuted classifier 1
        gets to ask a question the next time this function is run, then unmuted classifier 2 etc."""
        data = DC.getUnlabeledData()
        #calculate which classifiers arent muted and which turn it is
        i = 0
        userquery = None
        classifierasking = 0
        for j in xrange(0, len(self.classificationmodules)):
            if(j == self.poolbasedalclassifierturn + i):
                c = self.classificationmodules[j]
                if not c.isMuteClassificationModule(): 
                    userquery = c.calculatePoolBasedQuery(formula, data)
                    classifierasking = j 
                else:
                    i = i + 1
                    if (j == (len(self.classificationmodules) - 1) and userquery == None):
                    # bevor er wenn gar kein Classifier nicht gemutet ist in endlosschleife hängen bleibt
                    # nochmal kontrollieren vorm zurückspringen zum anfang
                        if any([c for c in self.classificationmodules if not c.isMuteClassificationModule()]):
                            self.poolbasedalclassifierturn = 0
                            return self.doPoolBasedALRound(formula, semisupervised, traininstantly)
                        else: raise Exception('Error, trying to do doPoolBasedALRound without a non-muted classifier')
        return [userquery, classifierasking]

    @classmethod
    def TestAllClassificationModules(self):
        """Tests all classification modules, they do that by themselves and return results to this function"""
        data = DC.getTestData()
        results = []
        for c in self.classificationmodules:
            results.append(c.test(data))
        return results

    @classmethod
    def PredictSingleSample(self, repolink):
        """Returns the sample with the probability and label each classification module would assign"""
        data = DC.getInformationsForRepo(repolink)
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
