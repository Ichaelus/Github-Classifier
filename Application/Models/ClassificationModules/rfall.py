#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Models.FeatureProcessing import *
import sklearn
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import abc
from ClassificationModule import ClassificationModule





class allrandomforest(ClassificationModule):
    """A basic Random Forest Classifier"""

    def __init__(self, text_corpus, filetype_corpus, foldername_corpus, reponame_lstm, n_estimators=200):
        ClassificationModule.__init__(self, "All Random Forest", "Ensemble Learner with multiple Decision-Trees")

        self.vectorizer = getTextVectorizer(1000) # Maximum of different columns
        self.filetypeVectorizer = getTextVectorizer(30) # TODO: Find better number
        self.foldernameVectorizer = getTextVectorizer(30) # TODO: Find better number

        # Vectorizer for descriptions and/or readmes
        corpus = []
        for text in text_corpus:
            corpus.append(process_text(text))
        self.vectorizer.fit(corpus)

        # Vectorizer for filetypes
        corpus = []
        for type in filetype_corpus:
            corpus.append(type)
        self.filetypeVectorizer.fit(corpus)

        # Vectorizer for foldernames
        corpus = []
        for folder in foldername_corpus:
            corpus.append(folder)
        self.foldernameVectorizer.fit(corpus)
        
        # Setup lstm for repository-name 
        """ Commented out as this is currently done in start.py already
        self.reponamelstm = reponame_lstm.loadClassificationModuleSavePoint("lastused")
        if (self.reponamelstm is None):
            self.reponamelstm = reponame_lstm
        """
        self.reponamelstm = reponame_lstm

        self.clf = RandomForestClassifier(n_estimators=n_estimators)
        
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
        return self.clf.fit(train_samples, train_lables)

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
        """Extract description and transform to vector"""
        sd = getDescription(sample)
        rm = getReadme(sample)
        arr = list(self.vectorizer.transform([sd, rm]).toarray()[0])
        arr += getMetadataVector(sample)
        arr += list(self.filetypeVectorizer.transform([getFiletypesString(sample)]).toarray()[0])
        arr += list(self.foldernameVectorizer.transform([getFoldernames(sample)]).toarray()[0])
        arr += self.reponamelstm.predictLabelAndProbability(sample)[1:]
        return np.asarray([arr])



