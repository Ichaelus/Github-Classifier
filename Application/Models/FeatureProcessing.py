#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################
# Convert repository information into features #
################################################

import cPickle as pickle
import os
import base64
import string

from sklearn.feature_extraction.text import TfidfVectorizer
import re
from nltk.stem import PorterStemmer
import numpy as np

from gensim.models import Word2Vec
import keras

# Constants

# TODO: Update values
max_stars = 1000
max_forks =  100
max_watches = 10
max_folder_count = 50
max_treeDepth = 10
max_branch_count = 10
max_forks = 50
max_commit_interval_avg = 10
max_contributors_count = 10
max_open_issues_count = 10
max_avg_commit_length = 100
max_file_count = 150
max_commit_interval_max = 20
max_commit_count = 200
max_readme_length = 1000 # TODO: What to do with this?
max_lev_files = 10 # Maximal Levenshtein distance
max_lev_folders = 10


max_vectorizer_word_count = 3000

possibleLanguages = ['JavaScript', 'Java', 'Python', 'C#', 'C++', 'Ruby', 
                    'CSS', 'C', 'Objective-C', 'Shell', 'Perl', 'PHP',
                    'R', 'CSS', 'HTML']

label_dict = {'DEV':0, 'HW':1, 'EDU':2, 'DOCS':3, 'WEB':4, 'DATA':5, 'OTHER':6}
class_weights = {0:1, 1:3, 2:3, 3:3, 4:3, 5:2, 6: 2}

# Save vectorizer so it doesnt have to be loaded from serialised file each time
global_vectorizer = None

def getClassWeights():
    """ Class Weight getter"""
    global class_weights
    return class_weights

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
        feature['description'] = getDescription(sample)
        if processText:
            feature['readme'] = process_text(feature['readme'])
            feature['description'] = process_text(feature['description'])
        features.append(feature)
        labels.append(getLabelIndex(sample[i]))
    return (features, labels, label_names)

def getLabelIndex(sample):
    """Returns the index for the class of a given sample"""
    assert  'class' in sample, "Data vector incomplete"
    global label_dict
    return label_dict[sample['class']]

def getLabelName(index):
    """Locates and returns the label for a given index"""
    for label in label_dict:
        if label_dict[label] == index:
            return label

    
def text_from_base64(input):
    """Convert text back from base64"""
    text = str(input).strip().replace('\\n', '') # Remove hardcoded newlines
#    print type(text)
    missing_padding = len(text) % 8
    if missing_padding != 0:
        text += b'='* (8 - missing_padding)
    try:
        text = base64.b64decode(text)
    except Exception as e:
        print "Error decoding text " + str(e)
        return ""
    return text

def getReadme(data):
    """Converts the base64 encoded readme into a text string"""
    assert  'readme' in data, "Data vector incomplete"
    return text_from_base64(data['readme'])

def getDescription(data):
    """Description value getter"""
    assert  'description' in data, "Data vector incomplete"
    return data['description']

def getReadmeLength(sample):
    """Returns the string length of the readme"""
    readme = getReadme(sample)
    return len(readme)

def getMetadataVector(sample):
    """ Get metadata """
    vec = []
    vec.append(min(1., float(sample['hasDownloads'])))
    vec.append(min(1., float(sample['watches']) / max_watches))
    vec.append(min(1., float(sample['folder_count']) / max_folder_count))
    vec.append(min(1., float(sample['treeDepth']) / max_treeDepth))
    vec.append(min(1., float(sample['stars']) / max_stars))
    vec.append(min(1., float(sample['branch_count']) / max_branch_count))
    vec.append(min(1., float(sample['forks']) / max_forks))
    vec.append(min(1., float(sample['commit_interval_avg']) / max_commit_interval_avg))
    vec.append(min(1., float(sample['contributors_count']) / max_contributors_count))
    vec.append(min(1., float(sample['open_issues_count']) / max_open_issues_count))
    vec.append(min(1., float(sample['avg_commit_length']) / max_avg_commit_length))
    vec.append(min(1., float(sample['hasWiki'])))
    vec.append(min(1., float(sample['file_count']) / max_file_count))
    vec.append(min(1., float(sample['commit_interval_max']) / max_commit_interval_max))
    vec.append(min(1., float(sample['isFork'])))
    vec.append(min(1., float(sample['commit_count']) / max_commit_count))
    vec.append(min(1., float(getReadmeLength(sample) / max_readme_length)))
    vec.append(min(1., float(avgLev(sample['folders']) / max_lev_folders)))
    vec.append(min(1., float(avgLev(sample['files']) / max_lev_files)))
    vec = vec + getLanguageVector(sample)
    return vec


def getMetadataLength():
    """Get length of Metadata Vector"""
    # TODO: Remove hardcoded answer
    return 19 + getLanguagesLength()

def getLanguageVector(sample):
    """Get vector of used languages"""
    # Some of the most popular languages on Github
    # TODO: Create better list
    global possibleLanguages

    vector = []
    # Index of each language is set to 0.5, of main language set to 1
    languageArray = sample['language_array'].split(' ')
    mainLanguage = sample['language_main']
    for language in possibleLanguages:
        if language == mainLanguage:
            vector.append(1.0)
        elif language in languageArray:
            vector.append(0.5)
        else:
            vector.append(0.0)
    return vector

def getLanguagesLength():
    global possibleLanguages
    return len(possibleLanguages)


def getFilenames(sample):
    """Returns string containing all filenames"""
    filenames = sample['files']
    """
    if filenames is not None:
        filenames = filenames.split(' ')
    else:
        filenames = []
        """
    return filenames

def getFiletypes(sample):
    """Returns a list of filetypes"""
    filetypes = []
    filenames = getFilenames(sample)
    for filename in filenames.split(' '):
        if '.' in filename:
            filetypes.append(filename.split('.')[-1])
    return list(set(filetypes))

def getFiletypesString(sample):
    """Converts the filetypes into a space separated string"""
    str = ""
    for filetype in getFiletypes(sample):
        str += filetype + ' '
    return str

def getFoldernames(sample):
    """Returns string containing all foldernames"""
    foldernames = sample.get('folders', '') # Returns FolderNames or empty string if not available
    return foldernames


def getFileNameAndAuthorString(sample):
    assert  'files' in sample and 'author' in sample, "Data vector incomplete"
    return (sample['files'], sample['author'])

def getTextVectorizer(max_features, vectorizer_name="vectorizer.bin"):
    """Creates new TfIdfVectorizer"""
    vectorizer = TfidfVectorizer(
                            sublinear_tf=True,  # Reason: 'It seems unlikely that twenty occurrences of a 
                                                # term in a document truly carry twenty times the significance of a single occurrence.'
                                                # http://nlp.stanford.edu/IR-book/html/htmledition/sublinear-tf-scaling-1.html
                            stop_words='english', # Removes Stopwords from document
                            decode_error='ignore', # Ignore if character couldnt be read
                            analyzer='word',    # Scan words, not characters
                            ngram_range=(1, 2), # Try different ngrams, possibly useful with more training data
                            max_features=max_features
                            #max_df=0.5 # Verwendet im ML-Kurs unter Preprocessing                   
                )
    return vectorizer


def process_text(text, remove_url=True, remove_code=True, remove_punctuation=True, stem=True):
    """Preprocess text (removing urls, punctuation etc.) bevore stemming and returning it"""
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

def getName(sample):
    return sample['name']

def getMetaAttMax(data):
    max_dict = dict()
    for c in data[0]:
        max_dict[c] = data[0][c]
    for sample in data:
        for c in sample:
            if sample[c] > max_dict[c]:
                max_dict[c] = sample[c]
    for c in max_dict:
        try:
            k = int(max_dict[c])
            print c, k
        except ValueError:
            continue
    
def oneHot(index):
    """Returns an array of 7 zeros and a 1 at index <index> """
    arr = np.zeros(7)
    arr[index] = 1
    return arr


# Stuff for LSTM
chars = string.ascii_lowercase + string.punctuation + string.digits + ' '
chars = sorted(set(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

def lstmEncode(C, maxlen=30):
    global chars, char_indices
    X = np.zeros((maxlen, len(chars)), np.uint8)
    for i, c in enumerate(C):
        if c.lower() not in chars:
            continue
        if i >= maxlen:
            break
        X[i, char_indices[c.lower()]] = 1
    return X

def lstmDecode(X):
    global indices_char
    X = X.argmax(axis=-1)
    return ''.join(indices_char[x] for x in X)

def getLstmCharLength():
    global chars
    return len(chars)

def getWord2VecModel():
    path= os.path.dirname(__file__) + "/../../Classifier_SavePoints/Word2Vec/"
    modelName = 'GoogleNews-vectors-negative300.bin'
    #if modelName not in os.listdir("../Classifier_SavePoints/Word2Vec"):
    #    print "Word2Vec-Model not found, try downloading from source"
    #    pass    # TODO: Actually implement downlaod
    #    return None
    return Word2Vec.load_word2vec_format(path + modelName, binary=True)

def resetWeights(kerasModel):
    """Resets weight of keras model"""
    assert type(kerasModel) == keras.models.Sequential, "Given object has to be of type Sequential."
    neuralNetworkWeights = kerasModel.get_weights()
    new_weights = []
    for w_layer in neuralNetworkWeights:
        m_shape = w_layer.shape
        new_l = np.random.uniform(-0.05, 0.05, m_shape)
        new_weights.append(new_l)
    kerasModel.set_weights(new_weights)
    

def avgLev(nameString):
    if nameString is None:
        return 0
    words = nameString.split(' ')
    if len(words) < 2:
        return 0
    dist = 0.0
    for i in xrange(len(words) - 1):
        dist += lev(words[i], words[i + 1])
    #print "Got one average distance!"
    return dist / (len(words) - 1)


def lev(source, target):
    """ Taken from https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python """
    if len(source) < len(target):
        return lev(target, source)

    # So now we have len(source) >= len(target).
    if len(target) == 0:
        return len(source)

    # We call tuple() to force strings to be used as sequences
    # ('c', 'a', 't', 's') - numpy uses them as values by default.
    source = np.array(tuple(source))
    target = np.array(tuple(target))

    # We use a dynamic programming algorithm, but with the
    # added optimization that we only need the last two rows
    # of the matrix.
    previous_row = np.arange(target.size + 1)
    for s in source:
        # Insertion (target grows longer than source):
        current_row = previous_row + 1

        # Substitution or matching:
        # Target and source items are aligned, and either
        # are different (cost of 1), or are the same (cost of 0).
        current_row[1:] = np.minimum(
                current_row[1:],
                np.add(previous_row[:-1], target != s))

        # Deletion (target grows shorter than source):
        current_row[1:] = np.minimum(
                current_row[1:],
                current_row[0:-1] + 1)

        previous_row = current_row

    return previous_row[-1]
