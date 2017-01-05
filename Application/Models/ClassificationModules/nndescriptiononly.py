#!/usr/bin/env python
# -*- coding: utf-8 -*-
from FeatureProcessing import *
from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.optimizers import Adam
import numpy as np
import abc
from ClassificationModule import ClassificationModule





class nndescriptiononly(ClassificationModule):
    """A basic feedforward neural network"""
    
    def __init__(self, text_corpus, num_hidden_layers=1):
        ClassificationModule.__init__(self, "Description only NN", "A basic feedforward neural network")
        # Create vectorizer and fit on all available Descriptions
        self.vectorizer = getTextVectorizer(3000) # Maximum of different columns
        corpus = []
        for description in text_corpus:
            corpus.append(process_text(description))
        self.vectorizer.fit(corpus)

        # Set input-size and output_size
        self.input_size = len(self.vectorizer.get_feature_names())
        self.output_size = 7 # Hardcoded for 6 classes

        # Create model
        model = Sequential()
        # Add input-layer
        model.add(Dense(self.input_size, input_dim=self.input_size, init='uniform'))
        model.add(Activation('relu'))

        # Add hidden layers
        for _ in xrange(num_hidden_layers):
            model.add(Dense(self.input_size, init='uniform'))
            model.add(Activation('relu'))
        
        # Add output layer and normalize probablities with softmax
        model.add(Dense(self.output_size, init='uniform'))
        model.add(Activation('softmax'))

        # Compile model and use Adam as optimizer
        model.compile(metrics=['accuracy'], loss='categorical_crossentropy', optimizer=Adam())

        self.model = model
        print "\t-", self.name


    def resetAllTraining(self):
        """Reset classification module to status before training"""
        resetWeights(self.model)

    def trainOnSample(self, sample, nb_epoch=1, shuffle=True, verbose=True):
        """Trainiere (inkrementell) mit Sample. Evtl zusätzlich mit best. Menge alter Daten, damit overfitten auf neue Daten verhindert wird."""
        description_vec = self.formatInputData(sample)
        label_index = getLabelIndex(sample)
        label_one_hot = np.expand_dims(oneHot(label_index), axis=0) # [1, 0, 0, ..] -> [[1, 0, 0, ..]] Necessary for keras
        self.model.fit(description_vec, label_one_hot, nb_epoch=nb_epoch, shuffle=shuffle, verbose=verbose) # TODO: think about nb_epoch-value

    def train(self, samples, nb_epoch=10, shuffle=True, verbose=True):
        """Trainiere mit Liste von Daten. Evtl weitere Paramter nötig (nb_epoch, learning_rate, ...)"""
        train_samples = []
        train_lables = []
        for sample in samples:
            formatted_sample = self.formatInputData(sample)[0].tolist()
            train_samples.append(formatted_sample)
            train_lables.append(oneHot(getLabelIndex(sample)))
        train_lables = np.asarray(train_lables)
        return self.model.fit(train_samples, train_lables, nb_epoch=nb_epoch, shuffle=shuffle, verbose=verbose, class_weight=getClassWeights())

    def predictLabel(self, sample):
        """Gibt zurück, wie der Klassifikator ein gegebenes Sample klassifizieren würde"""
        sample = self.formatInputData(sample)
        return np.argmax(self.model.predict(sample))
    
    def predictLabelAndProbability(self, sample):
        """Return the probability the module assignes each label"""
        sample = self.formatInputData(sample)
        prediction = self.model.predict(sample)[0]
        return [np.argmax(prediction)] + list(prediction) 

    def formatInputData(self, data):
        """Extract description and transform to vector"""
        sd = getDescription(data)
        # Returns numpy array which contains 1 array with features
        return self.vectorizer.transform([sd]).toarray()


