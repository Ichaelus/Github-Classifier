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
from nltk.stem import PorterStemmer
import string
import sklearn

# Constants
max_stars = 60000 # Max found in data was 52762
max_forks =  10000 # Max found in data was 9287
max_watches = 4000 # Max found in data was 3709

stemmer = PorterStemmer()

def one_hot_encoding(labels):
    # Get labels of type [1, 0, 2, ...] and convert to array
    # of type [[0, 1, 0, ..], [1, 0, 0, ..], [0, 0, 1, ...]]
    arr = np.zeros((len(labels), max(labels) + 1), np.uint8)
    arr[np.arange(len(labels)), labels] = 1
    return arr

def get_unlabeled_data(whatIWant='description'):
    # Standardmäßig wird NUR die description verwendet, nicht die readme

    #hole data als dict
    data = api_call(url="Gimme unlabeld pls")
    
    features = []

    for i in xrange(len(data)):
        feature = None
        if whatIWant == 'readme':
            #nur die readme ist anscheinend decoded
            feature = text_from_base64(data[i][whatIWant]).decode('utf-8')
        elif whatIWant == 'meta':
            """ 
            Availible metadata: description, author, url, tree, watches, 
                                class, languages, tagger, stars, readme, 
                                forks, id, name
            """
            feature = []
            sample = data[i]
            feature.append(float(sample['watches']) / max_watches)
            feature.append(float(sample['stars']) / max_stars)
            feature.append(float(sample['forks']) / max_forks)
            features.append(feature)
        else:
            feature = data[i][whatIWant]
        if whatIWant != 'meta':
            feature = process_text(feature)
        features.append(feature)
    return features
    
def text_from_base64(text):
    missing_padding = len(text) % 4
    if missing_padding != 0:
        text += b'='* (4 - missing_padding)
    text = None
    try:
        text = base64.b64decode(text)
    except TypeError:
        print "Error decoding readme"

    return text

def process_text(text):
    # Process string
    readme_codefree = ""
    words = ""
    final_words = ""
    if text is not None:
        for no_code in text.split("```")[::2]:
            # skip content code in e.g.  blalba```code```blabla
            readme_codefree += no_code
        #for word in readme_codefree.split():
        # Remove urls
        readme_urlfree = re.sub(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', ' ', readme_codefree)
        for word in ((char if char.isalpha() else " ") for char in readme_urlfree):
            try:
                words += word.decode('ascii')
            except UnicodeEncodeError:
                continue
        words = " ".join(words.split())
        for word in words.split():
            final_words += stemmer.stem(word) + " "

    return words

def shuffle_data(a, b):
    return sklearn.utils.shuffle(a, b)


def get_data(whatIWant='description', binary = False, equal=False):
    # Standardmäßig wird NUR die description verwendet, nicht die readme

    #hole data als dict
    data = api_call(equal=equal)
    #liste mit strings von den feature texten
    features = []
    #die namen der klassen
    label_names = []
    #die klassen
    labels = []

    # vectorizer braucht liste von strings, hier wirds umgewandelt
    for i in xrange(len(data)):
        feature = None
        if whatIWant == 'readme':
            #nur die readme ist anscheinend decoded
            try:
                feature = base64.b64decode(data[i][whatIWant])
            except TypeError:
                continue
            feature = feature.decode('utf-8')
        elif whatIWant == 'meta':
            """ 
            Availible metadata: description, author, url, tree, watches, 
                                class, languages, tagger, stars, readme, 
                                forks, id, name
            """
            feature = []
            sample = data[i]
            feature.append(float(sample['watches']) / max_watches)
            feature.append(float(sample['stars']) / max_stars)
            feature.append(float(sample['forks']) / max_forks)
            features.append(feature)
        else:
            feature = data[i][whatIWant]

        if whatIWant != 'meta':
            feature = process_text(feature)
        if binary:
            if data[i]['class'] == 'DEV':
                label = 'DEV'
            else:
                label = 'NOTDEV'
        else:
            label = data[i]['class']
        if label not in label_names:
            label_names.append(label)
        
        features.append(feature)
        labels.append(label_names.index(label))
        #if i % 50 == 0:
        #    print "{} repos processed".format(i)
    return (features, labels, label_names)

def get_batch(features, labels, nb_batch):
    x, y = shuffle_data(features, labels)
    return (x[:nb_batch], y[:nb_batch])


def api_call(equal=False):
    filter = base64.b64encode(b'id>0')
    url = None
    if equal:
        url = 'http://classifier.leimstaedtner.it/ajax.php?key=api:equal&filter='+filter.decode("utf-8")
    else:
        url = 'http://classifier.leimstaedtner.it/ajax.php?key=api:all&filter='+filter.decode("utf-8")
    request = Request(url)
    try:
        response = urlopen(request)
        data = json.load(response)
    except URLError, e:
        print 'Error with api call', e
    return data

# Nimmt die ersten ratio * 100% Elemente zum trainieren, Rest zum Testen
def split_train_test(features, labels, ratio=0.7, shuffle=False):
    cut = int(ratio * len(labels))
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
def vectorize_text(features, max_features=2000):
    vectorizer = TfidfVectorizer(sublinear_tf=True,
                            stop_words='english',
                            decode_error='strict',
                            analyzer='word',
                            max_features=max_features,
                            max_df=0.5 # Verwendet im ML-Kurs unter Preprocessing                   
                            )
    feature_vec = vectorizer.fit_transform(features)
    return feature_vec.toarray(), vectorizer

# wird im moment nicht verwendet, kann aber später hilfreich sein
#def get_synonyms(str):
	#synonyms = []
	#for syn in wn.synsets(str):
	    #for x in syn.lemmas():
	        #synonyms.append(x.name())
	#return synonyms
