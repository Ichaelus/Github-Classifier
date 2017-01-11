#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Models.FeatureProcessing import *

import sklearn
from sklearn.linear_model import LogisticRegression

import numpy as np
import abc
from ClassificationModule import ClassificationModule
from EnsembleClassifier import EnsembleClassifier



class lrstacking(EnsembleClassifier):
    """Ensemble Learning (Stacking) with Logistic Regression"""

    def __init__(self, classifiers):
        self.subclassifiers = []
        for classifier in classifiers:
            loadedClassifiers = classifier.loadClassificationModuleSavePoint()
            if loadedClassifiers is not None:
                self.subclassifiers.append(loadedClassifiers)
            else:
                self.subclassifiers.append(classifier)
        self.clf = LogisticRegression()
        EnsembleClassifier.__init__(self, "Logistic Regression Stacking", "Logistic Regression Stacking")
        print "\t-", self.name


    def resetAllTraining(self):
        """Reset classification module to status before training"""
        self.clf = sklearn.base.clone(self.clf)

    def trainOnSample(self, sample, nb_epoch=10, shuffle=True, verbose=True):
        """Trainiere (inkrementell) mit Sample. Evtl zusätzlich mit best. Menge alter Daten, damit overfitten auf neue Daten verhindert wird."""
        vec = self.formatInputData(sample)
        label_index = getLabelIndex(sample)
        return self.clf.fit(vec, np.expand_dims(label_index, axis=0))

    def train(self, samples, nb_epoch=10, shuffle=True, verbose=True):
        """Trainiere mit Liste von Daten. Evtl weitere Paramter nötig (nb_epoch, learning_rate, ...)"""
        train_samples = []
        train_lables = []
        for sample in samples:
            formatted_sample = self.formatInputData(sample)[0].tolist()
            train_samples.append(formatted_sample)
            train_lables.append(getLabelIndex(sample))
        train_lables = np.asarray(train_lables)
        return self.clf.fit(train_samples, train_lables)

    def predictLabel(self, sample):
        """Gibt zurück, wie der Klassifikator ein gegebenes Sample klassifizieren würde"""
        sample = self.formatInputData(sample)
        return self.clf.predict(sample)[0]
    
    def predictLabelAndProbability(self, sample):
        """Return the probability the module assignes each label"""
        sample = self.formatInputData(sample)
        prediction = self.clf.predict(sample)[0]
        return ([prediction] + oneHot(prediction).tolist())

    def formatInputData(self, sample):
        """Extract description and transform to vector"""
        predictions = []
        for classifier in self.subclassifiers:
            prediction = classifier.predictLabelAndProbability(sample)[1:]
            predictions += prediction
            """
            try: 
                prediction = classifier.predictLabelAndProbability(sample)
            except sklearn.exceptions.NotFittedError as e:
                print self.name, "tried to use an unfitted classifier", "(" + e.message + ")", "Make sure, there's a saved instance available "
                prediction = np.zeros(7).tolist()
            predictions += prediction        
            """
        # Returns numpy array which contains 1 array with features
        return np.expand_dims(predictions, axis=0)

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



