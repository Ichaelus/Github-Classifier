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

def moveRepoFromUnlabeledToToClassify(api_url):
    data = api_call('move&from_table=unlabeled&to_tabel=to_classify&api_url=' + api_url)
    return data

def moveRepoFromToClassifyToTrain(api_url, label):
    # moves <api_url> to train and assigns the given label
    data = api_call('move&from_table=to_classify&to_tabel=train&api_url=' + api_url + '&label=' + label)
    return data

def moveRepoFromUnlabeledToSemiSupervised(api_url, label):
    #label muss großgeschriebener String sein
    data = api_call('move&from_table=unlabeled&to_tabel=semisupervised&api_url=' + api_url + '&label=' + label)
    return data

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

def getTrainData():
    return api_call('all', tableString="train")

def getToClassifyCount():
    return str(api_call('all', tableString="to_classify"))

def getAllDescriptions():
    tables = ['train', 'to_classify']
    corpus = []

    for table in tables:
        data = api_call("all", tableString=table)
        for sample in data:
            corpus.append(sample['description'])
    return corpus

def getInformationsForRepo(repolink):
    '''Nur dafür da wenn ein bestimmtes Repo klassifiziert werden soll dass noch nicht in DB ist'''
    data = api_call('generate_sample&api-url=' + repolink)
    if(data == ""):
        raise Exception("Private Repository")
    # Check if api_call returned Error
    if(data.has_key('Error')):
        raise Exception(data['Error'])
    return data
