#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cPickle as pickle
import os
import base64

from sklearn.feature_extraction.text import TfidfVectorizer
import re
from nltk.stem import PorterStemmer

# Constants
max_stars = 60000 # Max found in data was 52762
max_forks =  10000 # Max found in data was 9287
max_watches = 4000 # Max found in data was 3709
max_folder_count = 1
max_treeDepth = 1
max_branch_count = 1
max_forks = 1
max_commit_interval_avg = 1
max_contributors_count = 1
max_open_issues_count = 1
max_avg_commit_length = 1
max_file_count = 1
max_commit_interval_max = 1

max_vectorizer_word_count = 3000

# Save vectorizer so it doesnt have to be loaded from serialised file each time
global_vectorizer = None

#besser: evtl in getunlabeleddata und getlabeleddata und gettrainingsdata aufspalten?
def getVectorsFromData(data, processText=True):
    """Get list of dicts which contain all feature-vectors"""
    # Feature vectors
    features = []
    # Klassennamen
    label_names = []
    # Classes
    labels = []

    for i in xrange(len(data)):
        sample = data[i]
        feature = {'readme':None, 'description':None, 'meta':None}
        feature['readme'] = getReadme(sample)
        feature['meta'] = getMetadataVector(sample)
        feature['description'] = getShortDescription(sample)
        if processText:
            feature['readme'] = process_text(feature['readme'])
            feature['description'] = process_text(feature['description'])
        label = data[i]['class']
        if label not in label_names:
            label_names.append(label)
        features.append(feature)
        labels.append(label_names.index(label))
    return (features, labels, label_names)
    
def text_from_base64(text):
    """Convert text back from base64"""
    missing_padding = len(text) % 4
    if missing_padding != 0:
        text += b'='* (4 - missing_padding)
    text = None
    try:
        text = base64.b64decode(text)
    except TypeError:
        print "Error decoding readme"
        return ""
    return text

def getReadme(data):
    return base64.b64decode(data['readme'])

def getShortDescription(data):
    return data['description']

def getMetadataVector(sample):
    # Get metadata
    vec = []
    vec.append(float(sample['hasDownloads']))
    vec.append(float(sample['watches']) / max_watches)
    vec.append(float(sample['folder_count']) / max_folder_count)
    vec.append(float(sample['treeDepth']) / max_treeDepth)
    vec.append(float(sample['stars']) / max_stars)
    vec.append(float(sample['branch_count']) / max_branch_count)
    vec.append(float(sample['forks']) / max_forks)
    vec.append(float(sample['commit_interval_avg']) / max_commit_interval_avg)
    vec.append(float(sample['contributors_count']) / max_contributors_count)
    vec.append(float(sample['open_issues_count']) / max_open_issues_count)
    vec.append(float(sample['avg_commit_length']) / max_avg_commit_length)
    vec.append(float(sample['hasWiki']))
    vec.append(float(sample['file_count']) / max_file_count)
    vec.append(float(sample['commit_interval_max']) / max_commit_interval_max)
    vec.append(float(sample['isFork']))
    return vec

def getFileNameAndAuthorString(sample):
    return (sample['files'], sample['author'])

def getTextVectorizer(vectorizer_name="vectorizer.bin"):
    """Creates new TfIdfVectorizer"""
    vectorizer = TfidfVectorizer(
                            sublinear_tf=True,  # Reason: 'It seems unlikely that twenty occurrences of a 
                                                # term in a document truly carry twenty times the significance of a single occurrence.'
                                                # http://nlp.stanford.edu/IR-book/html/htmledition/sublinear-tf-scaling-1.html
                            stop_words='english', # Removes Stopwords from document
                            decode_error='ignore', # Ignore if character couldnt be read
                            analyzer='word',    # Scan words, not characters
                            ngram_range=(1, 2), # Try different ngrams, possibly useful with more training data
                            max_features=max_vectorizer_word_count
                            #max_df=0.5 # Verwendet im ML-Kurs unter Preprocessing                   
                )
    return vectorizer


def process_text(text, remove_url=True, remove_code=True, remove_punctuation=True, stem=True):
    # Process string
    readme_codefree = ""
    readme = ""
    words = ""
    final_words = ""
    if text is not None:
        if remove_code is True:
            for no_code in text.split("```")[::2]:
                # skip content code in e.g.  blalba```code```blabla
                readme += no_code
        if remove_url:
            # Remove urls
            readme = re.sub(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', ' ', readme)
        if remove_punctuation:
            for word in ((char if char.isalpha() else " ") for char in readme):
                try:
                    words += word.decode('ascii')
                except UnicodeEncodeError:
                    continue
            words = " ".join(words.split())
        else:
            words = readme
        if stem:
            stemmer = PorterStemmer()
            for word in words.split():
                final_words += stemmer.stem(word) + " "
        else:
            final_words = words
    return final_words