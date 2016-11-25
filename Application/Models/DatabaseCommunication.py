#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
from urllib2 import Request, urlopen, URLError
import json

#hier drinnen muss sehr viel noch komplett überarbeitet werden

# Constants
max_stars = 60000 # Max found in data was 52762
max_forks =  10000 # Max found in data was 9287
max_watches = 4000 # Max found in data was 3709

def api_call(key, filterstring):
    """Get list of Repos-Data in json-format"""
    filterstring = base64.b64encode(b'' + filterstring)
    url = None
    data = None
    url = 'http://classifier.leimstaedtner.it/ajax.php?key=api:' + key.decode("utf-8") + '&filter=' + filterstring.decode("utf-8")
    request = Request(url)
    print url
    try:
        response = urlopen(request)
        data = json.load(response)
    except URLError, e:
        print 'Error with api call', e
    return data

#besser: evtl in getunlabeleddata und getlabeleddata und gettrainingsdata aufspalten?
def get_data(binary = False, no_dev=False):
    """Get list of dicts which contain all feature-vectors"""

    #hole data als dict
    data = api_call()

    # Feature vectors
    features = []
    # Klassennamen
    label_names = []
    # Classes
    labels = []

    for i in xrange(len(data)):
        sample = data[i]
        feature = dict()
        try:
            # Try to decode readme, continue without sample if there wa
            readme = base64.b64decode(sample['readme'])
        except TypeError:
            continue
        feature['readme'] = process_text(readme.decode('utf-8'))

        # Get metadata
        feature['meta'] = []
        feature['meta'].append(float(sample['hasDownloads']))
        feature['meta'].append(float(sample['watches']) / max_watches)
        feature['meta'].append(float(sample['folder_count']) / max_folder_count)
        feature['meta'].append(float(sample['treeDepth']) / max_treeDepth)
        feature['meta'].append(float(sample['stars']) / max_stars)
        feature['meta'].append(float(sample['branch_count']) / max_branch_count)
        feature['meta'].append(float(sample['forks']) / max_forks)
        feature['meta'].append(float(sample['commit_interval_avg']) / max_commit_interval_avg)
        feature['meta'].append(float(sample['contributors_count']) / max_contributors_count)
        feature['meta'].append(float(sample['open_issues_count']) / max_open_issues_count)
        feature['meta'].append(float(sample['avg_commit_length']) / max_avg_commit_length)
        feature['meta'].append(float(sample['hasWiki']))
        feature['meta'].append(float(sample['file_count']) / max_file_count)
        feature['meta'].append(float(sample['commit_interval_max']) / max_commit_interval_max)
        feature['meta'].append(float(sample['isFork']))
        
        # Get description
        feature['description'] = process_text(sample['description'])
        if binary:
            if data[i]['class'] == 'DEV':
                label = 'DEV'
            else:
                label = 'NOTDEV'
        else:
            label = data[i]['class']
        if not no_dev or label != 'DEV':
            if label not in label_names:
                label_names.append(label)
            features.append(feature)
            labels.append(label_names.index(label))
        #if i % 50 == 0:
        #    print "{} repos processed".format(i)
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
    return text

def moveRepoToLabeled(repoDbId):
    return 'NotImplemented' 

def moveRepoToTOClassify(repoDbId):
    return 'NotImplemented'

def getFeatureVectorForRepo(repolink):
    return 'NotImplemented'

def getLabeledData():
    return 'NotImplemented'

def getUnlabeledData():
    return 'NotImplemented'

def getUnlabeledSingleSample():
    return 'NotImplemented'

def getTestData():
    return 'NotImplemented'

def getLabeledCount():
    return 'NotImplemented'

def getUnlabeledCount():
    return api_call('count', "class=UNLABELED")

def getTestCount():
    return 'NotImplemented'

def getToClassifyCount():
    return 'NotImplemented'



