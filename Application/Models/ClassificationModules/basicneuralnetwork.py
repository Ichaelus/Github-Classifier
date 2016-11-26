#!/usr/bin/env python
# -*- coding: utf-8 -*-
from FeatureProcessing import *
from ClassificationModule import ClassificationModule
from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.optimizers import Adam
import numpy as np



class basicneuralnetwork(ClassificationModule):
    """A basic feedforward neural network"""

    description = "A basic feedforward neural network"
    
    def __init__(self, output_size, text_corpus, num_hidden_layers=3):

        # Create vectorizer and fit on all available Descriptions
        self.vectorizer = getTextVectorizer(3000) # Maximum of different columns
        corpus = []
        for description in text_corpus:
            corpus.append(process_text(description))
        self.vectorizer.fit(corpus)

        # Set input-size and output_size
        self.input_size = len(self.vectorizer.get_feature_names())
        self.output_size = output_size

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
        adam = Adam()
        model.compile(metrics=['accuracy'], loss='categorical_crossentropy', optimizer=adam)

        self.model = model
        print('Model build and ready')


    def resetAllTraining(self):
        """Reset classification module to status before training"""
        self.model.compile(metrics=['accuracy'], loss='categorical_crossentropy', optimizer=Adam())

    def trainOnSample(self, sample, nb_epoch=10, shuffle=True, verbose=True):
        """Trainiere (inkrementell) mit Sample. Evtl zusätzlich mit best. Menge alter Daten, damit overfitten auf neue Daten verhindert wird."""
        description_vec = self.formatInputData(sample)
        label_index = getLabelIndex(sample)
        label_one_hot = oneHot(label_index)
        self.model.fit(description_vec, label_one_hot, nb_epoch=nb_epoch, shuffle=shuffle, verbose=verbose) # TODO: think about nb_epoch-value

    def train(self, samples, lables, nb_epoch=10, shuffle=True, verbose=True):
        """Trainiere mit Liste von Daten. Evtl weitere Paramter nötig (nb_epoch, learning_rate, ...)"""
        self.model.fit(samples, lables, nb_epoch=nb_epoch, shuffle=shuffle, verbose=verbose)

    def predictLabel(self, sample):
        """Gibt zurück, wie der Klassifikator ein gegebenes Sample klassifizieren würde"""
        return np.argmax(self.model.predict(self.formatInputData(sample)))
    
    def predictLabelAndProbability(self, sample):
        """Return the probability the module assignes each label"""
        sample = self.formatInputData(sample)
        return self.model.predict(sample)

    def formatInputData(self, data):
        sd = getDescription(data)
        return self.vectorizer.transform(sd)
