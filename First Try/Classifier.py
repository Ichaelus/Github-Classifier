import utilities
from utilities import *
import cPickle as pickle

import numpy as np

from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression

import keras
from keras.models import Sequential
from keras.layers import Dense, Activation

# Remove later, used to surpress warning because of Linear Regressor
import warnings
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")

class Classifier():
    
    classifier_types = ["nn", "svm", "nb", "lr"]

    def __init__(self, clf_type, input_size=None, output_size=None):
        # Check if clf_type is correct
        if clf_type is None or not clf_type.lower() in Classifier.classifier_types:
            raise TypeError("Enter correct classifier type")
        if clf_type.lower() == 'nn':
            if input_size is None or output_size is None:
                print("Enter input_size and output_size to create neural network")
                return None
            self.output_size = output_size
            
            model = Sequential()
            model.add(Dense(input_size, input_dim=(input_size)))
            model.add(Activation('tanh'))
            model.add(Dense(input_size *  2))
            model.add(Activation('tanh'))
            model.add(Dense(input_size * 2))
            model.add(Activation('tanh'))
            
            # Output Layer, one neuron per class
            model.add(Dense(output_size))
            # Softmax zum Normalisieren der Werte
            model.add(Activation('softmax'))

            model.compile(metrics=['accuracy'], optimizer='sgd', loss='mse')
            self.model = model
        elif clf_type.lower() == 'svm':
            self.model = SVC()
        elif clf_type.lower() == 'nb':
            self.model = MultinomialNB()
        elif clf_type.lower() == 'lr':
            self.model = LinearRegression()
        
    def train(self, X, Y, nb_epoch=10, batch_size=1, get_accuracy=True):
        assert len(X) == len(Y)
        if type(self.model) == keras.models.Sequential:
            self.model.fit(X, one_hot_encoding(Y), nb_epoch=nb_epoch, batch_size=batch_size, verbose=False)
        else:
            self.model.fit(X, Y)
        print("Trained model successfully")
        print("Final accuracy on training-set: {}".format(self.evaluate(X, Y)))

    def evaluate(self, X, Y):
        assert len(X) == len(Y)
        correct = 0
        for i, x in enumerate(X):
            if self.predict(x) == Y[i]:
                correct += 1
        return (float(correct) / len(X))

    def predict(self, x):
        if type(self.model) == keras.models.Sequential:
            return np.argmax(self.model.predict(np.asarray([x]))[0])
        else:
            return self.model.predict([x])[0]
    
    
        
