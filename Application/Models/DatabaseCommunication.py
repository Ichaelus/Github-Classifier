#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
from urllib2 import Request, urlopen, URLError, quote
import json
import ClassificationModules.FeatureProcessing as FP

def api_call(keyString, filterString="", tableString="", limitString="", selector = "*"):
    """Get list of Repos-Data in json-format"""
    filterString = base64.b64encode(b'' + filterString)
    url = None
    data = None
    url = 'http://67.209.116.156/ajax.php?key=api:' + keyString.decode("utf-8") + '&filter=' + quote(filterString.decode("utf-8")) + '&table=' + quote(tableString.decode("utf-8")) + '&limit=' + quote(limitString.decode("utf-8")) + "&selector=" + quote(selector.decode("utf-8"))
    request = Request(url)
    try:
        response = urlopen(request)
        data = json.load(response)
        if not isinstance(data, dict):
            return data # int, string, whatever
        assert data["success"] == True, "Database error: " + data["message"] + "\nwith query url:" + url
    except URLError, e:
        print 'Error with api call', e
    return data["data"] # dict

def moveRepoFromUnlabeledToToClassify(api_url):
    return api_call('move&from_table=unlabeled&to_table=to_classify&api_url=' + quote(api_url))

def moveRepoFromToClassifyToTrain(api_url, label):
    # moves <api_url> to train and assigns the given label
    return api_call('move&from_table=to_classify&to_table=train&api_url=' + quote(api_url) + '&label=' + quote(label))

def moveRepoFromUnlabeledToSemiSupervised(api_url, label):
    #label muss großgeschriebener String sein
    return api_call('move&from_table=unlabeled&to_table=semisupervised&api_url=' + quote(api_url) + '&label=' + quote(label))

def getLabeledData():
    return api_call('all', tableString="labeled")

def getUnlabeledData():
    return api_call('all', tableString="unlabeled", limitString="400")

def getUnlabeledSingleSample():
    return api_call('single', tableString="unlabeled")

def getTestData(useExtendedTestSet):
    testSet = api_call('all', tableString="standard_test_samples")
    if(useExtendedTestSet):
        testSet += api_call('all', tableString="test")
    return testSet

def getLabeledCount():
    return api_call('count', tableString="labeled")

def getUnlabeledCount():
    return  api_call('count', tableString="unlabeled")

def getTestCount(useExtendedTestSet):
    testCount = api_call('count', tableString="standard_test_samples")
    if(useExtendedTestSet):
        testCount += api_call('count', tableString="test")
    return testCount

def getTrainData():
    return api_call('all', tableString="train") + api_call('all', tableString="standard_train_samples")

def getToClassifyCount():
    return api_call('all', tableString="to_classify")

def getAllDescriptions():
    tables = ['standard_train_samples', 'train', 'to_classify']
    corpus = []

    for table in tables:
        data = api_call("all", tableString=table)
        for sample in data:
            corpus.append(sample['description'])
    return corpus

def getAllReadmes():
    tables = ['standard_train_samples', 'train', 'to_classify']
    corpus = []

    for table in tables:
        data = api_call("all", tableString=table)
        for sample in data:
            rm = ""
            try:
                rm = base64.b64decode(sample['readme'])
            except TypeError:
                # If there was an error decoding the message, just ignore atm
                pass
            corpus.append(rm)
    return corpus

def getAllFilenames():
    tables = ['standard_train_samples', 'train', 'to_classify']
    corpus = []
    for table in tables:
        data = api_call("all", tableString=table)
        for sample in data:
            rm = ""
            try:
                rm = sample['files']
            except TypeError:
                # If there was an error decoding the message, just ignore atm
                pass
            corpus.append(rm)
    return corpus


def getAllFiletypes():
    tables = ['standard_train_samples', 'train', 'to_classify']
    corpus = []
    for table in tables:
        data = api_call("all", tableString=table)
        for sample in data:
            corpus.append(FP.getFiletypesString(sample))
    return corpus

def getCorpi():
    # Same as above, but in one iteration
    tables = ['standard_train_samples', 'train', 'to_classify']
    descriptionCorpus = []; readmeCorpus = []; filenameCorpus = []; filetypeCorpus = []; foldernameCorpus = []

    for table in tables:
        data = api_call("all", tableString=table, selector = "readme, files, description, folders")
        for sample in data:
            rm = ""; fn = ""; fts = ""; fn = ""
            try:
                rm = base64.b64decode(sample['readme'])
                fn = sample['files']
                fts = FP.getFiletypesString(sample)
                fn = FP.getFoldernames(sample)
            except TypeError:
                # If there was an error decoding the message, just ignore atm
                pass
            descriptionCorpus.append(sample['description'])
            readmeCorpus.append(rm)
            filenameCorpus.append(fn)
            filetypeCorpus.append(fts)
            foldernameCorpus.append(fn)
    return descriptionCorpus, readmeCorpus, filenameCorpus, filetypeCorpus, foldernameCorpus
    
def getInformationsForRepo(repoApiUrl):
    '''Nur dafür da wenn ein bestimmtes Repo klassifiziert werden soll dass noch nicht in DB ist'''
    return api_call('generate_sample&api_url=' + quote(repoApiUrl))

def getStats(table, t):
    q = "" if t == "numerical"  else "&string_attrs=true"
    return api_call('stats'+q, tableString=table)

def getDistributionArray(table, useExtendedTestSet):
    stats1 = api_call('class-count', tableString="standard_"+table.lower()+"_samples")
    if(table.lower() != 'test' or useExtendedTestSet):
        stats2 = api_call('class-count', tableString=table.lower())
        stats = []
        for val in stats1 + stats2:
            to_append = True
            for _t in stats:
                # Looks badly like n². To be improved
                if _t["class"] == val["class"]:
                    _t["count"] = int(_t["count"]) + int(val["count"])
                    to_append = False
                    break
            if to_append:
                stats.append(val)
        return stats
    return stats1