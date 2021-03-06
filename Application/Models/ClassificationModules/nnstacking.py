#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Models.FeatureProcessing import *
from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.layers.advanced_activations import LeakyReLU
from keras.optimizers import Adam
import numpy as np
import abc
from EnsembleClassifier import EnsembleClassifier



class nnstacking(EnsembleClassifier):
    """A basic feedforward neural network"""
    def __init__(self, subclassifiers):
        EnsembleClassifier.__init__(self, "Stacking NN", "This is our best and therefore final classifier.\
        The input to this shallow neural net comprises the predictions of various Support Vector Machines, Random Forests, Gradient Boosted Regression Trees and neural networks (LSTM and normal).\
        Most of them being trained on different feature-combinations.\
        Additionally we supply it with a hand selected subset of metadata for context.\
        For an in-depth explanation see the Documentation.\
        The input is followed by one hidden layer with a leaky (smoothed) ReLu-Activation.\
        Loss-function: categorical crossentropy, optimizer: Adam.") 

        self.subclassifiers = subclassifiers

        # Set input-size and output_size
        self.input_size = 7 * len(subclassifiers) + getReducedMetadataLength()
        self.output_size = 7 # Hardcoded for 7 classes
        self.hidden_size = self.input_size

        # Create model
        model = Sequential()
        # Add input-layer
        model.add(Dense(self.hidden_size, input_dim=self.input_size, init='uniform'))

        # Add hidden layer
        model.add(LeakyReLU())
        model.add(Dense(self.output_size, init='uniform'))
            
            

        # Add output layer and normalize probablities with softmax
        #model.add(Dense(self.output_size, init='uniform'))
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
        readme_vec = self.formatInputData(sample)
        label_index = getLabelIndex(sample)
        label_one_hot = np.expand_dims(oneHot(label_index), axis=0) # [1, 0, 0, ..] -> [[1, 0, 0, ..]] Necessary for keras
        self.model.fit(readme_vec, label_one_hot, nb_epoch=nb_epoch, shuffle=shuffle, verbose=verbose)

    def train(self, samples, nb_epoch=15, shuffle=True, verbose=True):
        """Trainiere mit Liste von Daten. Evtl weitere Paramter nötig (nb_epoch, learning_rate, ...)"""
        train_samples = []
        train_lables = []
        for sample in samples:
            formatted_sample = self.formatInputData(sample, trainingData=samples)[0].tolist()
            train_samples.append(formatted_sample)
            train_lables.append(oneHot(getLabelIndex(sample)))
        train_lables = np.asarray(train_lables)
        class_weights = {0:0.2, 1:0.58, 2:0.8, 3:0.4, 4:0.79, 5:1, 6: 0.2}
        train_result = self.model.fit(train_samples, train_lables, nb_epoch=nb_epoch, shuffle=shuffle, verbose=verbose, class_weight=class_weights)
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

    def formatInputData(self, sample, trainingData=None):
        """Extract description and transform to vector"""
        predictions = []
        for classifier in self.subclassifiers:
            if (not classifier.isTrained) and (trainingData is not None):
                classifier.train(trainingData)
            prediction = classifier.predictLabelAndProbability(sample)[1:]
            predictions += prediction
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
