import numpy as numpy
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
import os
from bs4 import BeautifulSoup
import nltk
import base64
import random
from utilities import *
import json
from urllib2 import Request, urlopen, URLError

# For synonyms, corpus must be downloaded first via nltk.download()
# filesize < 12 MB
# Probably not as useful as I hoped
from nltk.corpus import wordnet as wn


def text_from_base64(text):
    return base64.b64decode(text)

def api_call(url='http://classifier.leimstaedtner.it/ajax.php?key=api:all'):
    request = Request(url)
    try:
        response = urlopen(request)
        data = json.load(response)
    except URLError, e:
        print 'Error with api call', e
    return data


def split_train_test(features, labels, ratio=0.7):
    cut = int(ratio * len(features))
    features_train, labels_train = features[:cut], labels[:cut]
    features_test, labels_test = features[cut:], labels[cut:]
    
    return (features_train, features_test, labels_train, labels_test)

def get_feature_vec(features):
    vectorizer = TfidfVectorizer(sublinear_tf=True,
                            #stop_words='english',
                            decode_error='strict',
                            analyzer='word',
                            max_df=0.5 # Verwendet im ML-Kurs unter Preprocessing                   
                            )
    feature_vec = vectorizer.fit_transform(features)
    return feature_vec.toarray()

def get_synonyms(str):
	synonyms = []
	for syn in wn.synsets(str):
	    for x in syn.lemmas():
	        synonyms.append(x.name())
	return synonyms
