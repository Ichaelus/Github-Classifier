#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Models.FeatureProcessing import *

import sklearn

import numpy as np
import abc
from ClassificationModule import ClassificationModule
from EnsembleClassifier import EnsembleClassifier



class averageensemble(EnsembleClassifier):
    """Ensemble Learning by averaging predictions"""

    def __init__(self, classifiers):
        self.subclassifiers = []
        for classifier in classifiers:
            loadedClassifiers = classifier.loadClassificationModuleSavePoint()
            if loadedClassifiers is not None:
                self.subclassifiers.append(loadedClassifiers)
            else:
                self.subclassifiers.append(classifier)

        EnsembleClassifier.__init__(self, "Average Ensemble", "Averaging the predictions of subclassifiers.")
        print "\t-", self.name


    def resetAllTraining(self):
        """Reset classification module to status before training"""
        pass

    def trainOnSample(self, sample, nb_epoch=10, shuffle=True, verbose=True):
        """Trainiere (inkrementell) mit Sample. Evtl zusätzlich mit best. Menge alter Daten, damit overfitten auf neue Daten verhindert wird."""
        pass

    def train(self, samples, nb_epoch=10, shuffle=True, verbose=True):
        """Trainiere mit Liste von Daten. Evtl weitere Paramter nötig (nb_epoch, learning_rate, ...)"""
        for classifier in self.subclassifiers:
            if not classifier.isTrained:
                classifier.train(samples)
        return None

    def predictLabel(self, sample):
        """Gibt den Durchschnitt zurück, wie die Klassifikatoren ein gegebenes Sample klassifizieren würde"""
        return np.argmax(self.formatInputData(sample))
    
    def predictLabelAndProbability(self, sample):
        """Return the probability the module assignes each label"""
        pred = self.formatInputData(sample)
        return [np.argmax(pred)] + pred

    def formatInputData(self, sample, trainingData=None):
        """Extract description and transform to vector"""
        predictions = []
        for classifier in self.subclassifiers:
            if (not classifier.isTrained) and (trainingData is not None):
                classifier.train(trainingData)
            prediction = classifier.predictLabelAndProbability(sample)[1:]
            predictions.append(prediction)
        final_avg = np.zeros(7)
        for pred in predictions:
            for i, category in enumerate(pred):
                final_avg[i] += category
        final_avg /= 7.0
        return final_avg.tolist()

    def getSubClassifierNames(self):
        names = []
        for classifier in self.subclassifiers:
            names.append(classifier.name)
        return names

    def getSubClassifierDescription(self):
        descriptions = []
        for classifier in self.subclassifiers:
            descriptions.append(classifier.descriptions)
        return descriptions



