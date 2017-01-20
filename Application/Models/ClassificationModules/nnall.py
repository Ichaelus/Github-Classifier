#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Models.FeatureProcessing import *
from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.layers.advanced_activations import LeakyReLU
from keras.optimizers import Adam
import numpy as np
import abc
from ClassificationModule import ClassificationModule



class nnall(ClassificationModule):
    """A basic feedforward neural network"""
    def __init__(self, text_corpus, filetype_corpus, filename_corpus, foldername_corpus, num_hidden_layers=1):
        ClassificationModule.__init__(self, "All NN", "A basic feedforward neural network")

        self.vectorizer = getTextVectorizer(7000) # Maximum of different columns
        self.filetypeVectorizer = getTextVectorizer(30) # TODO: Find better number
        self.foldernameVectorizer = getTextVectorizer(150) # TODO: Find better number
        self.filenameVectorizer = getTextVectorizer(150) # TODO: Find better number

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

        # Vectorizer for filenames
        corpus = []
        for type in filename_corpus:
            corpus.append(type)
        self.filenameVectorizer.fit(corpus)

        # Vectorizer for foldernames
        corpus = []
        for folder in foldername_corpus:
            corpus.append(folder)
        self.foldernameVectorizer.fit(corpus)
        
        # Set input-size and output_size
        self.input_size = len(self.vectorizer.get_feature_names()) + getMetadataLength() + len(self.filetypeVectorizer.get_feature_names()) + len(self.foldernameVectorizer.get_feature_names()) + len(self.filenameVectorizer.get_feature_names())
        self.output_size = 7 # Hardcoded for 7 classes

        # Create model
        model = Sequential()
        # Add input-layer
        model.add(Dense(self.input_size, input_dim=self.input_size, init='uniform'))
        model.add(LeakyReLU())

        # Add hidden layers
        for _ in xrange(num_hidden_layers):
            model.add(Dense(self.input_size, init='uniform'))
            model.add(LeakyReLU())
        
        # Add output layer and normalize probablities with softmax
        model.add(Dense(self.output_size, init='uniform'))
        model.add(Activation('softmax'))

        # Compile model and use Adam as optimizer
        model.compile(metrics=['accuracy'], loss='categorical_crossentropy', optimizer=Adam(0.0025))

        self.model = model
        print "\t-", self.name


    def resetAllTraining(self):
        """Reset classification module to status before training"""
        resetWeights(self.model)

    def trainOnSample(self, sample, nb_epoch=1, shuffle=True, verbose=True):
        """Trainiere (inkrementell) mit Sample. Evtl zusätzlich mit best. Menge alter Daten, damit overfitten auf neue Daten verhindert wird."""
        readme_vec = self.formatInputData(sample)
        label_index = getLabelIndex(sample)
        label_one_hot = np.expand_dims(oneHot(label_index), axis=0) # [1, 0, 0, ..] -> [[1, 0, 0, ..]] Necessary for keras
        self.model.fit(readme_vec, label_one_hot, nb_epoch=nb_epoch, shuffle=shuffle, verbose=verbose)

    def train(self, samples, nb_epoch=15, shuffle=True, verbose=True):
        """Trainiere mit Liste von Daten. Evtl weitere Paramter nötig (nb_epoch, learning_rate, ...)"""
        train_samples = []
        train_lables = []
        for sample in samples:
            formatted_sample = self.formatInputData(sample)[0].tolist()
            train_samples.append(formatted_sample)
            train_lables.append(oneHot(getLabelIndex(sample)))
        train_lables = np.asarray(train_lables)
        train_result = self.model.fit(train_samples, train_lables, nb_epoch=nb_epoch, shuffle=shuffle, verbose=verbose, class_weight=getClassWeights())
        self.isTrained = True
        return train_result

    def predictLabel(self, sample):
        """Gibt zurück, wie der Klassifikator ein gegebenes Sample klassifizieren würde"""
        if not self.isTrained:
            return 0
        sample = self.formatInputData(sample)
        return np.argmax(self.model.predict(sample))
    
    def predictLabelAndProbability(self, sample):
        """Return the probability the module assignes each label"""
        if not self.isTrained:
            return [0, 0, 0, 0, 0, 0, 0, 0]
        sample = self.formatInputData(sample)
        prediction = self.model.predict(sample)[0]
        return [np.argmax(prediction)] + list(prediction) # [0] So 1-D array is returned

    def formatInputData(self, sample):
        """Extract description and transform to vector"""
        sd = getDescription(sample)
        rm = getReadme(sample)
        arr = list(self.vectorizer.transform([sd, rm]).toarray()[0])
        arr += getMetadataVector(sample)
        arr += list(self.filetypeVectorizer.transform([getFiletypesString(sample)]).toarray()[0])
        arr += list(self.foldernameVectorizer.transform([getFoldernames(sample)]).toarray()[0])
        arr += list(self.filenameVectorizer.transform([getFilenames(sample)]).toarray()[0])
        return np.asarray([arr])
