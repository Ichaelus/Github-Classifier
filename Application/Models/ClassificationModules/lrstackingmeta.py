#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Models.FeatureProcessing import *

import sklearn
from sklearn.linear_model import LogisticRegression

import numpy as np
import abc
from ClassificationModule import ClassificationModule
from EnsembleClassifier import EnsembleClassifier



class lrstackingmeta(EnsembleClassifier):
    """Ensemble Learning (Stacking) with Logistic Regression"""

    def __init__(self, classifiers):
        self.subclassifiers = []
        for classifier in classifiers:
            loadedClassifiers = classifier.loadClassificationModuleSavePoint()
            if loadedClassifiers is not None:
                self.subclassifiers.append(loadedClassifiers)
            else:
                self.subclassifiers.append(classifier)
        self.clf = LogisticRegression(class_weight='balanced')
        EnsembleClassifier.__init__(self, "Logistic Regression Stacking with Metadata", "Logistic Regression Stacking")
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
            formatted_sample = self.formatInputData(sample, trainingData=samples)[0].tolist()
            train_samples.append(formatted_sample)
            train_lables.append(getLabelIndex(sample))
        train_lables = np.asarray(train_lables)
        train_result = self.clf.fit(train_samples, train_lables)
        self.isTrained = True
        return train_result

    def predictLabel(self, sample):
        """Gibt zurück, wie der Klassifikator ein gegebenes Sample klassifizieren würde"""
        if not self.isTrained:
            return 0
        sample = self.formatInputData(sample)
        return self.clf.predict(sample)[0]
    
    def predictLabelAndProbability(self, sample):
        """Return the probability the module assignes each label"""
        if not self.isTrained:
            return [0, 0, 0, 0, 0, 0, 0, 0]
        sample = self.formatInputData(sample)
        prediction = self.clf.predict(sample)[0]
        return ([prediction] + oneHot(prediction).tolist())

    def formatInputData(self, sample, trainingData=None):
        """Extract description and transform to vector"""
        predictions = []
        for classifier in self.subclassifiers:
            if (not classifier.isTrained) and (trainingData is not None):
                classifier.train(trainingData)
            prediction = classifier.predictLabelAndProbability(sample)[1:]
            predictions += prediction
        # Returns numpy array which contains 1 array with features
        predictions += getReducedMetadata(sample)
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

