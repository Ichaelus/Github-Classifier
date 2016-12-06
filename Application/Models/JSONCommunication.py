#!/usr/bin/env python
# -*- coding: utf-8 -*-
import demjson
import json
import ClassificationModules.ClassificationModule
from collections import OrderedDict

def ConvertClassifierCollectionToJSON(classificationModules):
	classifiers = OrderedDict()
	for c in classificationModules:
		accuracy = formatClassifierAccuracy(c.getAccuracy())
		confusionMatrix = {'matrix': formatConfusionMatrix(c.getConfusionMatrix()), 'order': ["DEV", "HW", "EDU", "DOCS", "WEB", "DATA", "OTHER"]}
		classifiers[c.getName()] = {'accuracy':accuracy, 'description':c.getDescription(), 'confusionMatrix':confusionMatrix, 'yield':c.getYield(), 'active': not c.isMuteClassificationModule()}
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
	#				[	[],
	#					...
	#					[]
	#				],
	#			"order": ["DEV",...]
	#		}
	#		description: "A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.",
	#		yield: "81",
	#		active: true
	#	}}
	#}

def getFormulas():
	return '["Entropy-Based", "Least Confident", "Margin-Sampling"]'


def formatSinglePrediction(data, results):
	repo = {'repoName':data['name'], 'repoAPILink':data["api_url"]}
	classifiers = {}
	for cresult in results:
		classifiers[cresult[0]] = {'probability':formatProbabilities(cresult[1])}
	returndata = {'repo':repo, 'classifiersUnsure': True, 'classifiers':classifiers}
	return json.dumps(returndata)
	#return '{"repoName": "rName", "classifierResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}'

		# EXAMPLE
	# {
	#	"repo":	{repoName: "repoName","repoAPILink":""},
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
	repo = {'repoName':sample['name'], 'repoAPILink':sample['api_url']}
	semisupervised = {'SemiSupervisedSureEnough': bool(SemiSupervisedL), 'SemiSupervisedLabel': SemiSupervisedLabel}
	classifiers = {}
	for cresult in results:
		classifiers[cresult[0]] = {'probability':formatProbabilities(cresult[1]), 'uncertainty':cresult[2], 'unsure':bool(cresult[3])}
	returndata = {'repo':repo, 'classifiersUnsure':bool(unsure), 'semisupervised':semisupervised, 'classifiers':classifiers}
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
	repo = {'repoName':sample['name'], 'repoAPILink':sample['api_url']}
	classifiers = {}
	for cresult in resultsForUserQuery:
		classifiers[cresult[0]] = {'probability':formatProbabilities(cresult[1]), 'uncertainty':float(cresult[2])}
	returndata = {'repo':repo,'classifierAsking':classifierasking.getName(), 'classifiers':classifiers, 'classifiersUnsure':True}
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
	classifiers = {}
	for result in results:
		confusionMatrix = {'matrix': formatConfusionMatrix(result[1][2]), 'order': ["DEV", "HW", "EDU", "DOCS", "WEB", "DATA", "OTHER"]}
		classifiers[result[0]] = {'accuracy':formatClassifierAccuracy(result[1][1]), 'confusionMatrix': confusionMatrix, 'yield':float(result[1][0])}
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
	#			"order": ["DEV",...]
	#		}
	#		yield: "81",
	#	}}
	#}


def formatSingleClassificationTest(classifier, result):
	#??? wieso braucht es nochmal das result
	# alle daten werden doch im classifier gespeichert!
	#
	classifiers = {}
	confusionMatrix = {'matrix': formatConfusionMatrix(result[2]), 'order': ["DEV", "HW", "EDU", "DOCS", "WEB", "DATA", "OTHER"]}
	classifiers[classifier.getName()] = {'accuracy':formatClassifierAccuracy(result[1]), 'confusionMatrix': confusionMatrix, 'yield':float(result[0])}
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
	#			"order": ["DEV",...]
	#		}
	#		yield: "81",
	#	}}
	#}
def formatSavePoints(savePoints):
	savePointsOutput = {}
	for savePoint in savePoints:
		savePointsOutput[savePoint[0]] = {'accuracy':formatClassifierAccuracy(savePoint[1]), 'yield':savePoint[2]}
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

def formatClassifierAccuracy(classifieraccuracy):
	accuracies = []
	accuracies.append({'class':'DEV', 'val':float(classifieraccuracy['DEV'])})
	accuracies.append({'class':'HW', 'val':float(classifieraccuracy['HW'])})
	accuracies.append({'class':'EDU', 'val':float(classifieraccuracy['EDU'])})
	accuracies.append({'class':'DOCS', 'val':float(classifieraccuracy['DOCS'])})
	accuracies.append({'class':'WEB', 'val':float(classifieraccuracy['WEB'])})
	accuracies.append({'class':'DATA', 'val':float(classifieraccuracy['DATA'])})
	accuracies.append({'class':'OTHER', 'val':float(classifieraccuracy['OTHER'])})
	return accuracies

def formatRepo(repo):
	repo = {'repoName':sample['name'], 'repoAPILink':sample[api_url]}
	return repo

def formatConfusionMatrix(matrix):
	return matrix.tolist()