#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
from urllib2 import Request, urlopen, URLError
import json

def api_call(keyString, filterString="", tableString=""):
    """Get list of Repos-Data in json-format"""
    filterString = base64.b64encode(b'' + filterString)
    url = None
    data = None
    url = 'http://classifier.leimstaedtner.it/ajax.php?key=api:' + keyString.decode("utf-8") + '&filter=' + filterString.decode("utf-8") + '&table=' + tableString.decode("utf-8")
    request = Request(url)
    try:
        response = urlopen(request)
        data = json.load(response)
    except URLError, e:
        print 'Error with api call', e
    return data

def moveRepoFromUnlabeledToToClassify(sample):
    repoDBID = NotImplemented
    #...
    return 'NotImplemented' 

def moveRepoFromToClassifyToTrain(sample):
    repoDBID = NotImplemented
    #...
    return 'NotImplemented'

def getFeatureVectorForRepo(repolink):
    # Maybe check if it's an api link or repo link
    return 'NotImplemented'

def getLabeledData():
    return api_call('all', tableString="labeled")

def getUnlabeledData():
    return api_call('all', tableString="unlabeled")

def getUnlabeledSingleSample():
    return api_call('single', tableString="unlabeled")

def getTestData():
    return api_call('all', tableString="test")

def getLabeledCount():
    return str(api_call('count', tableString="labeled"))

def getUnlabeledCount():
    return  str(api_call('count', tableString="unlabeled"))

def getTestCount():
    return str(api_call('count', tableString="test"))

def getToClassifyCount():
    return str(api_call('all', tableString="to_classify"))

def getAllDescriptions():
    tables = ['test', 'train', 'to_classify']
    corpus = []

    for table in tables:
        data = api_call("all", tableString=table)
        for sample in data:
            corpus.append(sample['description'])
    return corpus

def getInformationsForRepo(repolink):
    '''Nur dafür da wenn ein bestimmtes Repo klassifiziert werden soll dass noch nicht in DB ist'''
    return 'NotImplemented'



