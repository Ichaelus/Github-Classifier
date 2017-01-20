#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string
from keras.models import Sequential
from keras.layers import Activation, Dense, LSTM
from keras.optimizers import SGD, Adam
import numpy as np
import abc
from ClassificationModule import ClassificationModule
from gensim.models import Word2Vec
from Models.FeatureProcessing import *


class readmew2vlstm(ClassificationModule):
    """A basic lstm neural network"""
    
    def __init__(self, num_hidden_layers=3):
        ClassificationModule.__init__(self, "Readme Only Word2Vec LSTM", "A LSTM reading the Readme word by word")

        hidden_size = 300
        self.maxlen = 1000

        print "\tLoading word2vec Model"
        path= os.path.dirname(__file__) + "/../../Word2VecModel/"
        modelName = 'GoogleNews-vectors-negative300.bin'
        self.word2vecModel = Word2Vec.load_word2vec_format(path + modelName, binary=True)

        # Set output_size
        self.output_size = 7 # Hardcoded for 7 classes

        model = Sequential()

        # Maximum of self.maxlen charcters allowed, each in one-hot-encoded array
        model.add(LSTM(hidden_size, input_shape=(self.maxlen, self.word2vecModel.vector_size)))

        for _ in range(num_hidden_layers):
            model.add(LSTM(hidden_size))

        model.add(Dense(self.output_size))
        model.add(Activation('softmax'))

        model.compile(loss='categorical_crossentropy',
                    optimizer=Adam(),
                    metrics=['accuracy'])

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

    def train(self, samples, nb_epoch=5, shuffle=True, verbose=True):
        """Trainiere mit Liste von Daten. Evtl weitere Paramter nötig (nb_epoch, learning_rate, ...)"""
        train_samples = []
        train_lables = []
        for sample in samples:
            formatted_sample = self.formatInputData(sample)
            train_samples.append(formatted_sample)
            train_lables.append(oneHot(getLabelIndex(sample)))
        train_lables = np.matrix(train_lables)
        train_samples_m = np.zeros((len(train_samples), self.maxlen, self.word2vecModel.vector_size))
        for i, col in enumerate(train_samples):
            train_samples_m[i] = col
        train_result = self.model.fit(train_samples_m, train_lables, nb_epoch=nb_epoch, shuffle=shuffle, verbose=verbose, class_weight=getClassWeights())
        self.isTrained = True
        return train_result

    def predictLabel(self, sample):
        """Gibt zurück, wie der Klassifikator ein gegebenes Sample klassifizieren würde"""
        if not self.isTrained:
            return 0
        sample = self.formatInputData(sample)
        sample = np.expand_dims(sample, axis=0)
        return np.argmax(self.model.predict(sample))
    
    def predictLabelAndProbability(self, sample):
        """Return the probability the module assignes each label"""
        if not self.isTrained:
            return [0, 0, 0, 0, 0, 0, 0, 0]
        sample = self.formatInputData(sample)
        sample = np.expand_dims(sample, axis=0) 
        prediction = self.model.predict(sample)[0]
        return [np.argmax(prediction)] + list(prediction) # [0] So 1-D array is returned

    def formatInputData(self, sample):
        """Extract description and transform to vector"""
        sd = getReadme(sample)
        fvec = np.zeros((self.maxlen, self.word2vecModel.vector_size))
        i = 0
        for i, word in enumerate(sd.split()):
            word = process_text(word)
            if i >= self.maxlen:
                break
            try:
                fvec[i] = (self.word2vecModel[word])
            except ValueError:
                fvec[i] = (np.zeros(self.word2vecModel.vector_size))
            except KeyError:
                # If word isn't in vocabulary
                fvec[i] = (np.zeros(self.word2vecModel.vector_size))
            except AttributeError:
                fvec[i] = (np.zeros(self.word2vecModel.vector_size))
        return fvec



