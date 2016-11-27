#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import cPickle as pickle
from datetime import datetime, date, time
import ActiveLearningSpecific as AL
from FeatureProcessing import getLabelIndex
import numpy as np

import xml.etree.ElementTree as ET
import os.path

class ClassificationModule:
    __metaclass__ = ABCMeta

    description = "Doesnt have a description yet"
    name = ""
    path = "" 	#must be relative to start.py
    muted = False
    binary = False
    Yield = 0.0
    Accuracy = {"DEV":0.0, "HW":0.0, "EDU":0.0, "DOCS":0.0, "WEB":0.0, "DATA":0.0, "OTHER":0.0}
    
    @classmethod
    def getDescription(self):
        """Return the description"""
        return self.description
    @classmethod
    def getYield(self):
        """Return the Yield"""
        return self.Yield
    
    @classmethod
    def getAccuracy(self):
        """Return the Accuracy"""
        return self.Accuracy

    @classmethod
    def setName(self, name):
        """Set name"""
        self.name = name

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
    def predictLabelAndProbability(self, sample): # According to docstring - Shouldnt this be called predictProbabilities?
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
        nb_right_pred = 0 # Number of right predictions
        class_count = np.zeros(7) # Number each class was found in data
        class_right_pred_count = np.zeros(7)

        for sample in data:
            pred_out = self.predictLabelAndProbability(self, data)
            # Check if prediction was right
            true_label_index = getLabelIndex(data)
            if (np.argmax(pred_out) == true_label_index):
                nb_right_pred += 1
                class_right_pred_count[true_label_index] += 1
            class_count[true_label_index] += 1
           
        global Yield, Accuracy
        Yield = nb_right_pred / len(data)

        class_acc = class_right_pred_count / class_count
        return [Yield] + class_acc.tolist()

    @classmethod
    def calculatePoolBasedQuery(self,formula, data):
        """Module goes trough each sample, calculates the uncertainty for it and returns the sample with the highest uncertainty"""
        uncertainties = []
        for sample in data:
            resultc = self.predictLabelAndProbability(self, sample)
            if(formula == 'Entropy-Based'):
                uncertainty = AL.calculateUncertaintyEntropyBased(resultc)
            elif(formula == "Least Confident"):
                uncertainty = AL.calculateUncertaintyLeastConfident(resultc)
            elif(formula == "Margin-Sampling"):
                uncertainty = AL.calculateUncertaintyMarginSampling(resultc)
            uncertainties.append(uncertainty)
        maxuncertainty = 0
        sampleindex = 0
        for uncertainty in uncertainties:
            if uncertainty > maxuncertainty:
                maxuncertainty = uncertainty
                sampleindex = uncertainties.index(uncertainty)
        return data[sampleindex]

	
    @classmethod
    def saveModule(self):
		"""serializes modul and add a savepoint to XML-File"""
		### require a xml-file which contains <data></data>
		###	at directory path
		#Serialization
		filename = datetime.now().isoformat() + '.pkl'
		tmpPath = os.path.abspath(".")
		tmpPath = os.path.join(tmpPath, self.path, filename)
		output = open(tmpPath, 'w')
		pickle.dump(ClassificationModule, output, 2)
		output.close()
		
		#XML-file
		tmpPath = os.path.abspath(".") 
		tmpPath = os.path.join(tmpPath, self.path, self.name + '.xml')
		tree = ET.parse(tmpPath)		
		root = tree.getroot()
	
		today = date.today()
		entry = ET.SubElement(root, 'version', {'name':filename})
		day = ET.SubElement(entry, 'day')
		day.text = str(today.day)
		month = ET.SubElement(entry, 'month')
		month.text = str(today.month)
		year = ET.SubElement(entry, 'year')
		year.text = str(today.year)
		#SubElement nimmt nur dicts aus strings
		stringDict = {}
		for key, value in self.Accuracy.iteritems():
			stringDict[str(key)] = str(value)
		ET.SubElement(entry, 'accuracy', stringDict)
        ElementYield = ET.SubElement(entry, 'yield')
        ElementYield.text = str(self.Yield)
		tree.write(tmpPath)
		return None
		
    @classmethod
    def getSavePointsForClassificationModules(self):
        ### require a xml-file which contains <data></data>
        ###	at directory path
        """holt aus dem XML File die möglichen SaveZustände"""
        tmpPath = os.path.abspath(".") 
        tmpPath = os.path.join(tmpPath, self.path, self.name + '.xml')
        tree = ET.parse(tmpPath)
        root = tree.getroot()
        savePoints = []
        for child in root:
            tmp = {}
            for i in xrange(0, len(child.find('accuracy').attrib.keys())):
                tmp[child.find('accuracy').attrib.keys()[i]] = child.find('accuracy').attrib.values()[i]
            savePoints.append([child.attrib.values()[0], tmp, float(child.find('yield').text)])
            #returns a list of tuples with filename and Accuracy
        return savePoints
		
		
    @classmethod
    def loadClassificationModuleSavePoint(self, filename="lastused"):
        ### require a xml-file which contains <data></data>
		###	at directory path
		#wenn lastused, dann wird aus dem XML-File der Name vom zuletzt benutzten SavePoint rausgesucht
		"""loads another SafePoint with filename of the current ClassificationModule"""
		if (filename is "lastused"):
			tmpPath = os.path.abspath(".") 
			tmpPath = os.path.join(tmpPath, self.path, self.name + '.xml')
			tree = ET.parse(tmpPath)
			root = tree.getroot()
			lastmodified = 'zzzzzzzzzzzzzzzzzzzzzz'  #Lexikographisch sehr schlechtes wort
													#quasi wie -unendlich bei Zahlensortierverfahren
			for child in root:
				tmp = child.attrib.values()[0]
				if (lastmodified > tmp):
					lastmodified = tmp
			if (lastmodified is "zzzzzzzzzzzzzzzzzzzzzz"):
				#there is no savepoint
				return None
			filename = lastmodified
		tmpPath = os.path.abspath(".")
		tmpPath = os.path.join(tmpPath, self.path, filename)
		f = open(tmpPath)
		data = pickle.load(f)
		#returned ein ClassificationModule
		return data


    