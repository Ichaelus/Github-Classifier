#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import cPickle as pickle
from datetime import datetime, date, time
import ActiveLearningSpecific as AL
from FeatureProcessing import getLabelIndex
import numpy as np
import re
import copy

import xml.etree.ElementTree as ET
import os

class ClassificationModule:
    __metaclass__ = ABCMeta

    def __init__(self, name, description):
        self.description = description
        self.name = name
        self.muted = False
        self.binary = False
        self.Yield = 0.0
        self.Accuracy = {"DEV":0.0, "HW":0.0, "EDU":0.0, "DOCS":0.0, "WEB":0.0, "DATA":0.0, "OTHER":0.0}

    
    def getDescription(self):
        """Return the description"""
        return self.description

    def getYield(self):
        """Return the Yield"""
        return self.Yield
    

    def getAccuracy(self):
        """Return the Accuracy"""
        return self.Accuracy.copy()


    def setName(self, name):
        """Set name"""
        self.name = name

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

    def muteClassificationModule(self):
        """The Module loses it´s right to give queries to the user"""
        self.muted = True

    def unmuteClassificationModule(self):
        """The Module gains the right back to give queries to the user"""
        self.muted = False

    def isMuteClassificationModule(self):
        """Returns if the module is muted or not"""
        return self.muted

    def isBinary(self):
        """Checks if classifier output is binary (dev/non_dev)"""
        return self.binary
    
    def setBinary(self, bin):
        """Set if classifier output is binary (dev/non_dev)"""
        self.binary = bin
    
    def testModule(self, data):
        """Module tests itself, refreshes yield and accuracy and returns data about these thests to the ClassifierCollection"""
        nb_right_pred = 0 # Number of right predictions
        class_count = np.zeros(7) # Number each class was found in data
        class_right_pred_count = np.zeros(7)

        for sample in data:
            pred_out = self.predictLabelAndProbability(sample)
            # Check if prediction was right
            true_label_index = getLabelIndex(sample)
            if (pred_out[0] == true_label_index):
                nb_right_pred += 1
                class_right_pred_count[true_label_index] += 1
            class_count[true_label_index] += 1
    
        if len(data) != 0:
            self.Yield = float(nb_right_pred) / len(data)
            class_acc = class_right_pred_count / class_count
            self.Accuracy['DEV'] = class_acc[0]
            self.Accuracy['HW'] = class_acc[1]
            self.Accuracy['EDU'] = class_acc[2]
            self.Accuracy['DOCS'] = class_acc[3]
            self.Accuracy['WEB'] = class_acc[4]
            self.Accuracy['DATA'] = class_acc[5]
            self.Accuracy['OTHER'] = class_acc[6]
        return [self.getYield(), self.getAccuracy()]

    def calculatePoolBasedQuery(self,formula, data):
        """Module goes trough each sample, calculates the uncertainty for it and returns the sample with the highest uncertainty"""
        uncertainties = []
        for sample in data:
            resultc = self.predictLabelAndProbability(sample)
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

    def saveModule(self):
        """serializes modul and add a savepoint to XML-File"""
        ###Folder building if necessary
        ###Serialization
        filename = datetime.now().isoformat().replace(":", "") + '.pkl'
        #generating a path that is indepentent from operating system
        tmpPath = self.getSavePath()
        tmpPath = os.path.join(tmpPath, self.name, filename)
        #save module
        output = open(tmpPath, 'wb')
        pickle.dump(self, output, 2)
        output.close()
        
        ###XML-file
        #generating a path that is indepentent from operating system
        tmpPath = self.getSavePath()
        tmpPath = os.path.join(tmpPath, self.name, self.name + '.xml')
        tree = ET.parse(tmpPath)
        root = tree.getroot()
        #write information about module into ElementTree-object
        today = date.today()
        entry = ET.SubElement(root, 'version', {'name':filename})
        day = ET.SubElement(entry, 'day')
        day.text = str(today.day)
        month = ET.SubElement(entry, 'month')
        month.text = str(today.month)
        year = ET.SubElement(entry, 'year')
        year.text = str(today.year)
        #SubElement can only handle dicts out of strings => transformation necessary
        stringDict = {}
        for key, value in self.Accuracy.iteritems():
            stringDict[str(key)] = str(value)
        ET.SubElement(entry, 'accuracy', stringDict)
        ElementYield = ET.SubElement(entry, 'yield')
        ElementYield.text = str(self.Yield)
        #save XML-File
        tree.write(tmpPath)
        return None
        
    def getSavePointsForClassificationModules(self):
        ### require a xml-file which contains <data></data>
        ###	at directory path
        """holt aus dem XML File die möglichen SaveZustände"""
        #generating a path that is indepentent from operating system
        tmpPath = self.getSavePath()
        tmpPath = os.path.join(tmpPath, self.name, self.name + '.xml')
        #open and convert XML-File to ElementTree-object
        tree = ET.parse(tmpPath)
        root = tree.getroot()
        savePoints = []
        for child in root:
            moduleAccuracy = {}
            for i in xrange(0, len(child.find('accuracy').attrib.keys())):
                moduleAccuracy[child.find('accuracy').attrib.keys()[i]] = float(child.find('accuracy').attrib.values()[i])
            savePoints.append([child.attrib.values()[0], moduleAccuracy, float(child.find('yield').text)])
        #return: list of lists of element0: filename, element1: dict for Accuracy and element2: yield
        #       [['2016-11-28T18:38:10.221000.pkl', {"DEV":0.0, "HW":0.0, ...}, 90.93], ...]
        return savePoints
        
    def loadClassificationModuleSavePoint(self, filename="lastused"):
        ### require a xml-file which contains <data></data>
        ###	at directory path
        #wenn lastused, dann wird aus dem XML-File der Name vom zuletzt benutzten SavePoint rausgesucht
        """loads another SafePoint with filename of the current ClassificationModule"""
        if (filename is "lastused"):
            #generating a path that is indepentent from operating system
            tmpPath = self.getSavePath()
            tmpPath = os.path.join(tmpPath, self.name, self.name + '.xml')
            #open and convert XML-File to ElementTree-data
            lastmodified = "000000"  #Lexikographisch sehr gutes wort
                                #quasi wie -unendlich bei Zahlensortierverfahren
            lastmodifiedOutNumbersLetters = "000000"
            tree = ET.parse(tmpPath)
            root = tree.getroot()
            #search for last saved file
            for child in root:
                tmp = child.attrib.values()[0]
                namelettersnumbers = re.sub("[^0-9a-zA-Z\s]", '', tmp)
                if (lastmodifiedOutNumbersLetters < namelettersnumbers):
                    lastmodifiedOutNumbersLetters = namelettersnumbers
                    lastmodified = tmp
            if (lastmodified is "000000"):
                #there is no savepoint
                return None
            filename = lastmodified
            #generating a path that is indepentent from operating system
        tmpPath = self.getSavePath()
        tmpPath = os.path.join(tmpPath, self.name, filename)
        #deserialization
        f = open(tmpPath, 'rb')
        data = pickle.load(f)
        #return: ClassificationModule or None if there isnt one
        return data
    
    def tryNewDirForModule(self, savepath):
        """builds a new directory and xml-file if it doesnt exit"""
        #generating a path that is indepentent from operating system
        if (os.path.exists(savepath) == False):
            #building new Folder
            os.mkdir(savepath)  
        tmpPath = os.path.join(savepath, self.name)
        if (os.path.exists(tmpPath) == False):
            #building new Folder
            os.mkdir(tmpPath)       # throws a  OSError if path already exits
            #building XML-SaveInfoFile
        tmpPath = os.path.join(tmpPath, self.name + '.xml')
        if  os.path.exists(tmpPath) == False:
            d = open(tmpPath, "w")
            d.write("<data></data>\n")
            d.close()

    def getSavePath(self):
        """Returns the basic path to the save folder"""
        #ensure savepath exists
        savepath = os.path.abspath(__file__)
        savepath = os.path.join(savepath, os.pardir)
        savepath = os.path.join(savepath, os.pardir)
        savepath = os.path.join(savepath, os.pardir)
        savepath = os.path.abspath(os.path.join(savepath, "Classifier_SavePoints"))
        self.tryNewDirForModule(savepath)
        return savepath
