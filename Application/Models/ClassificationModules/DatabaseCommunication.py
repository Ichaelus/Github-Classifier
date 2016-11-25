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

def moveRepoToLabeled(repoDbId):
    return 'NotImplemented' 

def moveRepoToTOClassify(repoDbId):
    return 'NotImplemented'

def getFeatureVectorForRepo(repolink):
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
    return api_call('count', tableString="labeled")

def getUnlabeledCount():
    return api_call('count', tableString="unlabeled")

def getTestCount():
    return api_call('count', tableString="test")

def getToClassifyCount():
    return api_call('all', tableString="to_classify")



