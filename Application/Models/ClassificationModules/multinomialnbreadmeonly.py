#!/usr/bin/env python
# -*- coding: utf-8 -*-
from FeatureProcessing import *
import sklearn
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import abc
from ClassificationModule import ClassificationModule





class multinomialnbreadmeonly(ClassificationModule):
    """A Multinomial Naive Bayes"""
    
    def __init__(self, text_corpus):
        ClassificationModule.__init__(self, "Readme Only Multinomial Naive Bayes", "A Multinomial Naive Bayes-Classifier")
        # Create vectorizer and fit on all available Descriptions
        self.vectorizer = getTextVectorizer(5000) # Maximum of different columns
        corpus = []
        for description in text_corpus:
            corpus.append(process_text(description))
        self.vectorizer.fit(corpus)

        self.clf = MultinomialNB()
        print "\t-", self.name


    def resetAllTraining(self):
        """Reset classification module to status before training"""
        self.clf = sklearn.base.clone(self.clf)

    def trainOnSample(self, sample, shuffle=True, verbose=True):
        """Trainiere (inkrementell) mit Sample. Evtl zusätzlich mit best. Menge alter Daten, damit overfitten auf neue Daten verhindert wird."""
        readme_vec = self.formatInputData(sample)
        label_index = getLabelIndex(sample)
        return self.clf.fit(readme_vec, np.expand_dims(label_index, axis=0))

    def train(self, samples, shuffle=True, verbose=True):
        """Trainiere mit Liste von Daten. Evtl weitere Paramter nötig (nb_epoch, learning_rate, ...)"""
        train_samples = []
        train_lables = []
        for sample in samples:
            formatted_sample = self.formatInputData(sample)[0].tolist()
            train_samples.append(formatted_sample)
            train_lables.append(getLabelIndex(sample))
        train_lables = np.asarray(train_lables)
        return self.clf.fit(train_samples, train_lables, class_weight = 'auto')

    def predictLabel(self, sample):
        """Gibt zurück, wie der Klassifikator ein gegebenes Sample klassifizieren würde"""
        sample = self.formatInputData(sample)
        return self.clf.predict(sample)[0]
    
    def predictLabelAndProbability(self, sample):
        """Return the probability the module assignes each label"""
        sample = self.formatInputData(sample)
        prediction = self.clf.predict_proba(sample)[0]
        return [np.argmax(prediction)] + list(prediction) 

    def formatInputData(self, sample):
        """Extract readme and transform to vector"""
        sd = getReadme(sample)
        # Returns numpy array which contains 1 array with features
        return self.vectorizer.transform([sd]).toarray()


