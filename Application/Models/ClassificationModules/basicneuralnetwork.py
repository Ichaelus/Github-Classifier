#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ClassificationModule import ClassificationModule
from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.optimizers import Adam

import numpy as np



class basicneuralnetwork(ClassificationModule):
    """A basic feedforward neural network"""

    description = "A basic feedforward neural network"
    
    def __init__(self, input_size, output_size, num_hidden_layers=3):
        model = Sequential()
        # Add input-layer
        model.add(Dense(input_size, input_dim=input_size, init='uniform'))
        model.add(Activation('relu'))
        
        # Add hidden layers
        for _ in xrange(num_hidden_layers):
            model.add(Dense(input_size, init='uniform'))
            model.add(Activation('relu'))
        
        # Add output layer and normalize probablities with softmax
        model.add(Dense(output_size, init='uniform'))
        model.add(Activation('softmax'))

        # Compile model and use Adam as optimizer
        adam = Adam()
        model.compile(metrics=['accuracy'], loss='categorical_crossentropy', optimizer=adam)

        self.model = model

        print('Model build and ready')

    
    def resetAllTraining(self):
        """Reset classification module to status before training"""
        pass

    def trainOnSample(self, sample, nb_epoch=10, shuffle=True, verbose=True):
        """Trainiere (inkrementell) mit Sample. Evtl zusätzlich mit best. Menge alter Daten, damit overfitten auf neue Daten verhindert wird."""
        x = np.expand_dims(sample, axis=0)
        self.model.fit(x, nb_epoch=nb_epoch, shuffle=shuffle, verbose=verbose) # TODO: think about nb_epoch-value


    def train(self, samples, classes, nb_epoch=10, shuffle=True, verbose=True):
        """Trainiere mit Liste von Daten. Evtl weitere Paramter nötig (nb_epoch, learning_rate, ...)"""
        self.model.fit(samples, classes, nb_epoch=nb_epoch, shuffle=shuffle, verbose=verbose)

    def predictLabel(self, sample):
        """Gibt zurück, wie der Klassifikator ein gegebenes Sample klassifizieren würde"""
        return np.argmax(self.model.predict(sample))
    
    def predictLabelAndProbability(self, sample):
        """Return the probability the module assignes each label"""
        return self.model.predict(sample) # First element as keras returns list of detailed predictions

    def formatInputData(self):
        pass
