#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Models.FeatureProcessing import *
import sklearn
from sklearn.ensemble import AdaBoostClassifier
import numpy as np
import abc
from ClassificationModule import ClassificationModule





class metaonlyadaboost(ClassificationModule):
    """An AdaBoostClassifier with Decision-Trees as Base Estimator"""

    def __init__(self):
        ClassificationModule.__init__(self, "Meta Only AdaBoostClassifier (Descision-Trees)", 'AdaBoostClassifier (base estimator: Decision-Trees) used with Meta-Data (Programming-Languages, stars, watches, ...)')
        self.clf = AdaBoostClassifier()
        print "\t-", self.name


    def resetAllTraining(self):
        """Reset classification module to status before training"""
        self.clf = sklearn.base.clone(self.clf)

    def trainOnSample(self, sample, nb_epoch=10, shuffle=True, verbose=True):
        """Trainiere (inkrementell) mit Sample. Evtl zusätzlich mit best. Menge alter Daten, damit overfitten auf neue Daten verhindert wird."""
        readme_vec = self.formatInputData(sample)
        label_index = getLabelIndex(sample)
        return self.clf.fit(readme_vec, np.expand_dims(label_index, axis=0))

    def train(self, samples, nb_epoch=10, shuffle=True, verbose=True):
        """Trainiere mit Liste von Daten. Evtl weitere Paramter nötig (nb_epoch, learning_rate, ...)"""
        train_samples = []
        train_lables = []
        for sample in samples:
            formatted_sample = self.formatInputData(sample)[0].tolist()
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
        prediction = self.clf.predict_proba(sample)[0]
        return [np.argmax(prediction)] + list(prediction)

    def formatInputData(self, sample):
        """Extract description and transform to vector"""
        sd = getMetadataVector(sample)
        # Returns numpy array which contains 1 array with features
        return np.expand_dims(sd, axis=0)


