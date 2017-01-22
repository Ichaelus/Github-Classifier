#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Models.FeatureProcessing import *
import sklearn
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
import abc
from ClassificationModule import ClassificationModule





class gbrtdescriptionmeta(ClassificationModule):
    """A Gradient Tree Boosting Classifier """

    def __init__(self, text_corpus, n_estimators=150):
        description = "Here 150 base classifiers are being used to predict \
        the class based on meta-features as well as the short-description which gets encoded by a Tfidf-Vectorizer (Vocabulary Size: 6000)."

        ClassificationModule.__init__(self, "Description and Metadata Gradient Tree Boosting", description)

        # Create vectorizer and fit on all available Descriptions
        self.vectorizer = getTextVectorizer(6000) # Maximum of different columns/ words
        corpus = []
        for description in text_corpus:
            corpus.append(process_text(description))
        self.vectorizer.fit(corpus)

        self.clf = GradientBoostingClassifier(n_estimators=n_estimators)
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
        sd = getDescription(sample)
        vec = list(self.vectorizer.transform([sd]).toarray()[0])
        vec += list(getMetadataVector(sample))
        # Returns numpy array which contains 1 array with features
        return np.asarray([vec])

