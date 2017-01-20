#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################
# A collection of Python -> JSON conversion  functions #
########################################################

from collections import OrderedDict
import json
import demjson
import Models.ClassificationModules.ClassificationModule
import Models.classifierMeasures as CM

def ConvertClassifierCollectionToJSON(classificationModules):
    """Not there"""
    classifiers = OrderedDict()
    for c in classificationModules:
        Precision = formatClassifierPrecision(c.getPrecision())
        matrix = c.getConfusionMatrix()
        measures = {
            'Precision mu': CM.precision_mu(matrix),
            'Recall mu': CM.recall_mu(matrix),
            'Fscore mu': CM.fscore_mu(matrix, 0.5),
            'Average Accuracy': CM.avg_accuracy(matrix),
            'Error Rate': CM.err_rate(matrix),
            'Precision M': CM.precision(matrix),
            'Recall M': CM.recall(matrix),
            'Fscore M': CM.fscore(matrix, 0.5),
        }
        confusionMatrix = {
            'matrix': formatConfusionMatrix(matrix),
            'measures': measures,
            'order': ["DEV", "HW", "EDU", "DOCS", "WEB", "DATA", "OTHER"],
        }
        classifiers[c.getName()] = {
            'active': not c.isMuteClassificationModule(),
            'confusionMatrix':confusionMatrix,
            'description':c.getDescription(),
            'isTrained': c.isTrained,
            'precision':Precision,
        }
    returndata = {'classifiers': classifiers}
    return json.dumps(returndata)
    #return '{"classifiers": {"Neural network1": {"description":"A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.","yield":0.81,"active":true,"uncertainty": 0.5,"result":[{"class":"DEV","val":0.0},{"class":"HW","val":0.0},{"class":"EDU","val":0.0},{"class":"DOCS","val":0.0},{"class":"WEB","val":0.0},{"class":"DATA","val":0.0},{"class":"OTHER","val":0.0}]},"Neural network2":{"description":"A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.","yield":0.55,"uncertainty": 0.5,"active":false,"result":[{"class":"DEV","val":0.0},{"class":"HW","val":0.0},{"class":"EDU","val":0.0},{"class":"DOCS","val":0.0},{"class":"WEB","val":0.0},{"class":"DATA","val":0.0},{"class":"OTHER","val":0.0}]},"Neural network3":{"description":"A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.","yield":0.90,"uncertainty": 0.5,"active":true,"result":[{"class":"DEV","val":0.0},{"class":"HW","val":0.0},{"class":"EDU","val":0.0},{"class":"DOCS","val":0.0},{"class":"WEB","val":0.0},{"class":"DATA","val":0.0},{"class":"OTHER","val":0.0}]}}}'
    # EXAMPLE
    # {classifiers:{
    # 	"<ModuleName>" : {
    #		accuracy:[
    #			{class: "DEV", val : 0.04},
    #			{class: "HW", val : 0.13},
    #			{class: "EDU", val : 0.11},
    #			{class: "DOCS", val : 0.24},
    #			{class: "WEB", val : 0.59},
    #			{class: "DATA", val : 0.02},
    #			{class: "OTHER", val : 0.04}
    #		],
    #		"confusionMatrix":{
    #			"matrix":
    #				[	[val11,...		  val1N, 		totalRow, 	percentageRow],
    #					...
    #					[valM1,...		  valMN, 		totalRow, 	percentageRow],
    #					[totalCol,...     totalCol, 	TOTAL, 		""],
    #					[percentageCol,...percentageCol, "", 	percentageTOTAL]
    #				],
    #			"order": ["DEV",...],
    #			/* Table 3 @ http://rali.iro.umontreal.ca/rali/sites/default/files/publis/SokolovaLapalme-JIPM09.pdf */
    #			"measures": {
    #							"Average Accuracy" : 0.3,
    #							"Error Rate" : 0.1,
    #							"Precision mu" : 0.5,
    #							"Recall mu" : 0.1,
    #							"Fscore mu" : 0.6,
    #                           "Precision M": 0.3,
    #                           "Recall M": 0.7,
    #                           "Fscore M": 0.44,
    #						}
    #		}
    #		description: "A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.",
    #		yield: "81",
    #		active: true
    #	}}
    #}

def getFormulas():
    """Missing DocString"""
    return '["Entropy-Based", "Least Confident", "Margin-Sampling"]'


def formatSinglePrediction(data, results):
    """Missing DocString"""
    classifiers = {}
    for cresult in results:
        classifiers[cresult[0]] = {'probability':formatProbabilities(cresult[1])}
    returndata = {'repo':formatRepo(data), 'classifiersUnsure': True, 'classifiers':classifiers}
    return json.dumps(returndata)
        # EXAMPLE
    # {
    #	"repo":	{repoName: "repoName","repoAPILink":"",..},
    #	"classifiers":{
    # 	"<ModuleName>" : {
    #		probability:[
    #			{class: "DEV", val : 0.04},
    #			{class: "HW", val : 0.13},
    #			{class: "EDU", val : 0.11},
    #			{class: "DOCS", val : 0.24},
    #			{class: "WEB", val : 0.59},
    #			{class: "DATA", val : 0.02},
    #			{class: "OTHER", val : 0.04}
    #		]	
    #	}}
    #}

    

#hier fehlt noch die uncertainty von jedem classifier jeweils
def formatStreamBasedALRound(sample, unsure, SemiSupervisedL, SemiSupervisedLabel, results):
    """Missing DocString"""
    semisupervised = {
        'SemiSupervisedSureEnough': bool(SemiSupervisedL),
        'SemiSupervisedLabel': SemiSupervisedLabel,
        }
    classifiers = {}
    for cresult in results:
        classifiers[cresult[0]] = {
            'probability':formatProbabilities(cresult[1]),
            'uncertainty':float(cresult[2]),
            'unsure':bool(cresult[3]),
            }
    returndata = {
        'repo':formatRepo(sample),
        'classifiersUnsure':bool(unsure),
        'semisupervised':semisupervised,
        'classifiers':classifiers,
        }
    return json.dumps(returndata)

    #return '{"repo": {"repoName": "rName", "repoAPILink":""}, "classifiersUnsure":"true","semisupervised":{"SemiSupervisedSureEnough":"false","SemiSupervisedLabel":"None"} ,"classifierResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}'
    # EXAMPLE
    # {
    #	"repo":{repoName: "repoName","repoAPILink":""},
    #	"classifiersUnsure":"true",
    #	"semisupervised":{"SemiSupervisedSureEnough":"false","SemiSupervisedLabel":"None"},
    #	classifiers:{
    # 	"<ModuleName>" : {
    #		probability:[
    #			{class: "DEV", val : 0.04},
    #			{class: "HW", val : 0.13},
    #			{class: "EDU", val : 0.11},
    #			{class: "DOCS", val : 0.24},
    #			{class: "WEB", val : 0.59},
    #			{class: "DATA", val : 0.02},
    #			{class: "OTHER", val : 0.04}
    #		],
    #		uncertainty: 0.5
    #		unsure: false
    #	}}
    #}

#wollen wir hier von allen classifiern die uncertainties zum ausgewählten sample angeben?
def formatPoolBasedALRound(sample, classifierasking, resultsForUserQuery):
    classifiers = {}
    for cresult in resultsForUserQuery:
        classifiers[cresult[0]] = {
            'probability':formatProbabilities(cresult[1]),
            'uncertainty':float(cresult[2]),
            }
    returndata = {
        'repo':formatRepo(sample),
        'classifierAsking':classifierasking.getName(),
        'classifiers':classifiers,
        'classifiersUnsure':True,
        }
    return json.dumps(returndata)
    #return '{"repo":{"repoName": "rName", "repoAPILink":""}, "classifierAsking":"Neural Network1","classifierResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}'
    # EXAMPLE
    # {
    # "repo":{repoName: "repoName","repoAPILink":""},
    # "classifierAsking":"Neural Network1",
    # "classifiersUnsure": true,
    # "classifiers":{
    # 	"<ModuleName>" : {
    #		"probability":[
    #			{class: "DEV", val : 0.04},
    #			{class: "HW", val : 0.13},
    #			{class: "EDU", val : 0.11},
    #			{class: "DOCS", val : 0.24},
    #			{class: "WEB", val : 0.59},
    #			{class: "DATA", val : 0.02},
    #			{class: "OTHER", val : 0.04}
    #		],
    #		uncertainty: 0.5
    #	}}
    #}

#falls wirs als array von formatSingleClassificationTest machen, ansonsten muss das wieder anders ausschaun
def formatMultipleClassificationTests(results):
    """No DOC string"""
    classifiers = {}
    for result in results:
        measures = {
            'Precision mu': CM.precision_mu(result[1][1]),
            'Recall mu': CM.recall_mu(result[1][1]),
            'Fscore mu': CM.fscore_mu(result[1][1], 0.5),
            'Average Accuracy': CM.avg_accuracy(result[1][1]),
            'Error Rate': CM.err_rate(result[1][1]),
            'Precision M': CM.precision(result[1][1]),
            'Recall M': CM.recall(result[1][1]),
            'Fscore M': CM.fscore(result[1][1], 0.5),
            }
        confusionMatrix = {
            'matrix': formatConfusionMatrix(result[1][1]),
            'measures': measures,
            'order': ["DEV", "HW", "EDU", "DOCS", "WEB", "DATA", "OTHER"],
            }
        classifiers[result[0]] = {
            'precision':formatClassifierPrecision(result[1][0]),
            'confusionMatrix': confusionMatrix,
            }
    returndata = {'classifiers':classifiers}
    return json.dumps(returndata)	
    #return '[ { "name" : "blub", "yield" : 0.84, "classifierResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}, { "name" : "blub2", "yield" : 0.84, "classifierResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}]'
    # EXAMPLE
    # {classifiers:{
    # 	"<ModuleName>" : {
    #		accuracy:[
    #			{class: "DEV", val : 0.04},
    #			{class: "HW", val : 0.13},
    #			{class: "EDU", val : 0.11},
    #			{class: "DOCS", val : 0.24},
    #			{class: "WEB", val : 0.59},
    #			{class: "DATA", val : 0.02},
    #			{class: "OTHER", val : 0.04}
    #		],
    #		"confusionMatrix":{
    #			"matrix":
    #				[	[],
    #					...
    #					[]
    #				],
    #			"order": ["DEV",...],
    #           "measures": {
    #							"Average Accuracy" : 0.3,
    #							"Error Rate" : 0.1,
    #							"Precision mu" : 0.5,
    #							"Recall mu" : 0.1,
    #							"Fscore mu" : 0.6,
    #                           "Precision M": 0.3,
    #                           "Recall M": 0.7,
    #                           "Fscore M": 0.44,
    #						}
    #		}
    #		yield: "81",
    #	}}
    #}


def formatSingleClassificationTest(classifier, result):
    #??? wieso braucht es nochmal das result
    # alle daten werden doch im classifier gespeichert!
    #
    classifiers = {}
    measures = {
        'Precision mu': CM.precision_mu(result[1]),
        'Recall mu': CM.recall_mu(result[1]),
        'Fscore mu': CM.fscore_mu(result[1], 0.5),
        'Average Accuracy': CM.avg_accuracy(result[1]),
        'Error Rate': CM.err_rate(result[1]),
        'Precision M': CM.precision(result[1]),
        'Recall M': CM.recall(result[1]),
        'Fscore M': CM.fscore(result[1], 0.5),
        }
    confusionMatrix = {
        'matrix': formatConfusionMatrix(result[1]),
        'measures': measures,
        'order': ["DEV", "HW", "EDU", "DOCS", "WEB", "DATA", "OTHER"],
        }
    classifiers[classifier.getName()] = {
        'confusionMatrix': confusionMatrix,
        'isTrained': classifier.isTrained,
        'precision':formatClassifierPrecision(result[0]),
        }
    returndata = {'classifiers':classifiers}
    return json.dumps(returndata)
    #return '[ { "name" : "blub", "yield" : 0.84, "classifierResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}]'

    # EXAMPLE
    # {classifiers:{
    # 	"<ModuleName>" : {
    #		accuracy:[
    #			{class: "DEV", val : 0.04},
    #			{class: "HW", val : 0.13},
    #			{class: "EDU", val : 0.11},
    #			{class: "DOCS", val : 0.24},
    #			{class: "WEB", val : 0.59},
    #			{class: "DATA", val : 0.02},
    #			{class: "OTHER", val : 0.04}
    #		],
    #		"confusionMatrix":{
    #			"matrix":
    #				[	[],
    #					...
    #					[]
    #				],
    #			"order": ["DEV",...],
    #           "measures": {
    #							"Average Accuracy" : 0.3,
    #							"Error Rate" : 0.1,
    #							"Precision mu" : 0.5,
    #							"Recall mu" : 0.1,
    #							"Fscore mu" : 0.6,
    #                           "Precision M": 0.3,
    #                           "Recall M": 0.7,
    #                           "Fscore M": 0.44,
    #						}
    #		}
    #		yield: "81",
    #	}}
    #}
def formatSavePoints(savePoints):
    """Missing DocString"""
    savePointsOutput = {}
    for savePoint in savePoints:
        savePointsOutput[savePoint[0]] = {
            'precision':formatClassifierPrecision(savePoint[1])
            }
    returndata = {'savepoints': savePointsOutput}
    return json.dumps(returndata)
    #return '[ { "name" : "blub", "yield" : 0.84, "classifierResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}, { "name" : "blub2", "yield" : 0.84, "classifierResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}, { "name" : "blub3", "yield" : 0.84, "classifierResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}]'
    # EXAMPLE
    # {savepoints:{
    # 	"<filename>" : {
    #		accuracy:[
    #			{class: "DEV", val : 0.04},
    #			{class: "HW", val : 0.13},
    #			{class: "EDU", val : 0.11},
    #			{class: "DOCS", val : 0.24},
    #			{class: "WEB", val : 0.59},
    #			{class: "DATA", val : 0.02},
    #			{class: "OTHER", val : 0.04}
    #		],
    #		yield: "81",
    #	}}
    #}

#Hilfsunktionen für oben
def formatProbabilities(results):
    cprobabilities = []
    cprobabilities.append({'class':'DEV', 'val': float(results[1])})
    cprobabilities.append({'class':'HW', 'val': float(results[2])})
    cprobabilities.append({'class':'EDU', 'val': float(results[3])})
    cprobabilities.append({'class':'DOCS', 'val': float(results[4])})
    cprobabilities.append({'class':'WEB', 'val': float(results[5])})
    cprobabilities.append({'class':'DATA', 'val': float(results[6])})
    cprobabilities.append({'class':'OTHER', 'val': float(results[7])})
    return cprobabilities

def formatClassifierPrecision(classifierprecision):
    precision = []
    precision.append({'class':'DEV', 'val':float(classifierprecision['DEV'])})
    precision.append({'class':'HW', 'val':float(classifierprecision['HW'])})
    precision.append({'class':'EDU', 'val':float(classifierprecision['EDU'])})
    precision.append({'class':'DOCS', 'val':float(classifierprecision['DOCS'])})
    precision.append({'class':'WEB', 'val':float(classifierprecision['WEB'])})
    precision.append({'class':'DATA', 'val':float(classifierprecision['DATA'])})
    precision.append({'class':'OTHER', 'val':float(classifierprecision['OTHER'])})
    return precision

def formatRepo(sample):
    repo = {
        'repoName':sample['name'],
        'repoAPILink':sample["api_url"], 
        'author': sample['author'],
        'description': sample['description'],
        'file_count': sample['file_count'],
        'folder_count': sample['folder_count'],
        'commit_count': sample['commit_count'],
        'language': sample['language_main']
    }
    return repo

def formatConfusionMatrix(matrix):
    return matrix.tolist()

def formatStats(data):
    return json.dumps(data)

def toJson(x):
    return json.dumps(x)