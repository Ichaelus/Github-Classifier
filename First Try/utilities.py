# -*- coding: utf-8 -*-
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import os
#import nltk
import base64
import random
import json
from urllib2 import Request, urlopen, URLError
import re


def one_hot_encoding(labels):
    # Zur Zeit des Tests war nicht garantiert, dass alle 7 Klassen vertreten waren
    # One Hot Encoding muss aber für Models immer gleiche Anzahl an Spalten haben
    arr = np.zeros((len(labels), 7), np.uint8)
    arr[np.arange(len(labels)), labels] = 1
    return arr

def text_from_base64(text):
    return base64.b64decode(text)

def process_text(text):

    return text

def shuffle_data(x_train, y_train):
    x = list(zip(x_train, y_train))
    random.shuffle(x)
    x_train, y_train = zip(*x)
    return x_train, y_train


def get_data(whatIWant='description'):
    # Standardmäßig wird NUR die description verwendet, nicht die readme

    #hole data als dict
    data = api_call()
    #liste mit strings von den feature texten
    texts = []
    #die namen der klassen
    label_names = []
    #die klassen
    labels = []
    # vectorizer braucht liste von strings, hier wirds umgewandelt
    for i in xrange(len(data)):
        if whatIWant == 'readme':
            #nur die readme ist anscheinend decoded
            text = text_from_base64(data[i][whatIWant])
        text = data[i][whatIWant]
        #text = text.replace('\n', ' ')
        texts.append(text)
        label = data[i]['class']
        if label not in label_names:
            label_names.append(label)
        labels.append(label_names.index(label))
    return (texts, labels, label_names)


def api_call(url='http://classifier.leimstaedtner.it/ajax.php?key=api:all'):
    request = Request(url)
    try:
        response = urlopen(request)
        data = json.load(response)
    except URLError, e:
        print 'Error with api call', e
    return data

#nimmt die ersten ratio * 100% elemente zum trainieren, rest zum testen
def split_train_test(features, labels, ratio=0.7, shuffle=True):
    cut = int(ratio * len(features))
    features_train, labels_train = features[:cut], labels[:cut]
    features_test, labels_test = features[cut:], labels[cut:]
    
    # Shuffle data for better training results
    if shuffle:
        features_train, labels_train = shuffle_data(features_train, labels_train)
    
    return (features_train, features_test, labels_train, labels_test)

# wandelt text in matrix um, stop_words sind die ausfilterung 
# von unwichtigen wörtern
# https://de.wikipedia.org/wiki/Tf-idf-Maß
# http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
def vectorize_text(features):
    vectorizer = TfidfVectorizer(sublinear_tf=True,
                            stop_words='english',
                            decode_error='strict',
                            analyzer='word',
                            max_df=0.5 # Verwendet im ML-Kurs unter Preprocessing                   
                            )
    feature_vec = vectorizer.fit_transform(features)
    return feature_vec.toarray()

# wird im moment nicht verwendet, kann aber später hilfreich sein
#def get_synonyms(str):
	#synonyms = []
	#for syn in wn.synsets(str):
	    #for x in syn.lemmas():
	        #synonyms.append(x.name())
	#return synonyms
