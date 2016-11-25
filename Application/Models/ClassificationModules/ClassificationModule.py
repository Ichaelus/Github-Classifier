#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import cPickle as pickle
from datetime import datetime, date, time
import ActiveLearningSpecific as AL

class ClassificationModule:
    __metaclass__ = ABCMeta

    description = "Doesnt have a description yet"
    name = ""
    muted = False
    binary = False
    Yield = 0.0
    Accuracy = {"DEV":0.0, "HW":0.0, "EDU":0.0, "DOCS":0.0, "WEB":0.0, "DATA":0.0, "OTHER":0.0}
  
    @classmethod
    def getDescription(self):
        """Return the description"""
        return self.description

    @classmethod
    def getName(self):
        """Return the name"""
        return self.name
    
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
        """Trainiere mit mehreren Daten. Evtl weitere Paramter nötig (nb_epoch, learning_rate, ...)"""
        pass

    @abstractmethod
    def predictLabel(self, sample):
        """Gibt zurück, wie der Klassifikator ein gegebenes Sample klassifizieren würde"""
        pass
    
    @abstractmethod
    def predictLabelAndProbability(self, sample):
        """Return the probability the module assignes each label"""
        pass

    @abstractmethod
    def formatInputData(self):
        """Format data into the form the given classifier needs it, using functions from FeatureProcessing.py"""
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

    @classmethod
    def isBinary(self):
        """Checks if classifier output is binary (dev/non_dev)"""
        return self.binary
    
    @classmethod
    def setBinary(self, bin):
        """Set if classifier output is binary (dev/non_dev)"""
        self.binary = bin
    
    @classmethod
    def testModule(self, data):
        """Module tests itself, refreshes yield and accuracy and returns data about these thests to the ClassifierCollection"""
        return "NotImplemented"

    @classmethod
    def calculatePoolBasedQuery(self,formula, data):
        """Module goes trough each sample, calculates the uncertainty for it and returns the sample with the highest uncertainty"""
        uncertainties = []
        for sample in data:
            resultc = NotImplemented
            if(formula == 'Entropy-Based'):
                uncertainty = AL.calculateUncertaintyEntropyBased(resultc)
            elif(formula == "Least Confident"):
                uncertainty = AL.calculateUncertaintyLeastConfident(resultc)
            elif(formula == "Margin-Sampling"):
                uncertainty = AL.calculateUncertaintyMarginSampling(resultc)
            uncertainties.append(uncertainty)
        max = 0
        for uncertainty in uncertainties:
            if uncertainty > max:
                max = uncertainty
        sampleindex = uncertainties.index(uncertainty)
        return "NotImplemented"

	
    @classmethod
    def saveModule(self):
		""""""
		#Serialization
		filename = datetime.now().isoformat() + '.pkl'
		output = open(filename, 'w')
		pickle.dump(ClassificationModule, output, 2)
		output.close()
		#XML-file
		### filestruktur einbauen! es gibt einen Ordner für alle Module
		### im Ordner steckt ein XML file
		return None
		
    @classmethod
    def GetSavePointsForClassificationModules(self):
		"""holt aus dem XML File die möglichen SaveZustände"""
		pass
		#returned irgendwas mit filename mit zugehöriger Erkennungsgenauigkeit
    @classmethod
    def LoadClassificationModuleSavePoint(self, filename="lastused"):
        #wenn lastused, dann wird aus dem XML-File der Name vom zuletzt benutzten SavePoint rausgesucht
		"""loads another SafePoint with filename of the current ClassificationModule"""
		pass
		#returned ein ClassificationModule



    