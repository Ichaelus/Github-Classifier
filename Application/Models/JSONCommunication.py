#!/usr/bin/env python
# -*- coding: utf-8 -*-
import demjson
import json
import ClassificationModules.ClassificationModule

def ConvertClassifierCollectionToJSON(classificationModules):
	classificators = {}
	for c in classificationModules:
		accuracy = formatClassificatorAccuracy(c.getAccuracy())
		classificators[c.getName()] = {'result':accuracy, 'description':c.getDescription(), 'yield':c.getYield(), 'active': not c.isMuteClassificationModule()}
	returndata = {'classificators': classificators}
	return json.dumps(returndata)
	#return '{"classificators": {"Neural network1": {"description":"A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.","yield":0.81,"active":true,"uncertainty": 0.5,"result":[{"class":"DEV","val":0.0},{"class":"HW","val":0.0},{"class":"EDU","val":0.0},{"class":"DOCS","val":0.0},{"class":"WEB","val":0.0},{"class":"DATA","val":0.0},{"class":"OTHER","val":0.0}]},"Neural network2":{"description":"A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.","yield":0.55,"uncertainty": 0.5,"active":false,"result":[{"class":"DEV","val":0.0},{"class":"HW","val":0.0},{"class":"EDU","val":0.0},{"class":"DOCS","val":0.0},{"class":"WEB","val":0.0},{"class":"DATA","val":0.0},{"class":"OTHER","val":0.0}]},"Neural network3":{"description":"A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.","yield":0.90,"uncertainty": 0.5,"active":true,"result":[{"class":"DEV","val":0.0},{"class":"HW","val":0.0},{"class":"EDU","val":0.0},{"class":"DOCS","val":0.0},{"class":"WEB","val":0.0},{"class":"DATA","val":0.0},{"class":"OTHER","val":0.0}]}}}'
	# EXAMPLE
	# {classificators:{
	# 	"<ModuleName>" : {
	#		result:[
	#			{class: "DEV", val : 0.04},
	#			{class: "HW", val : 0.13},
	#			{class: "EDU", val : 0.11},
	#			{class: "DOCS", val : 0.24},
	#			{class: "WEB", val : 0.59},
	#			{class: "DATA", val : 0.02},
	#			{class: "OTHER", val : 0.04}
	#		],
	#		description: "A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.",
	#		yield: "81",
	#		active: true
	#	}}
	#}

def getFormulas():
	return '["Entropy-Based", "Least Confident", "Margin-Sampling"]'


def formatSinglePrediction(data, results):
	repo = {'repoName':data['name'], 'repoAPILink':data["api_url"]}
	classificators = {}
	for cresult in results:
		classificators[cresult[0]] = {'result':formatProbabilities(cresult[1])}
	returndata = {'repo':repo, 'classificators':classificators}
	return json.dumps(returndata)
	#return '{"repoName": "rName", "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}'

		# EXAMPLE
	# {
	#	"repo":	{repoName: "repoName","repoAPILink":""},
	#	"classificators":{
	# 	"<ModuleName>" : {
	#		result:[
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
	classificators = {}
	for cresult in results:
		classificators[cresult[0]] = {'result':formatProbabilities(cresult[1]), 'uncertainty':cresult[2], 'unsure':bool(cresult[3])}
	returndata = {'repo':repo, 'classifiersUnsure':bool(unsure), 'semisupervised':semisupervised, 'classificators':classificators}
	return json.dumps(returndata)
	#return '{"repo": {"repoName": "rName", "repoAPILink":""}, "classifiersUnsure":"true","semisupervised":{"SemiSupervisedSureEnough":"false","SemiSupervisedLabel":"None"} ,"classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}'
	# EXAMPLE
	# {
	#	"repo":{repoName: "repoName","repoAPILink":""},
	#	"classifiersUnsure":"true",
	#	"semisupervised":{"SemiSupervisedSureEnough":"false","SemiSupervisedLabel":"None"},
	#	classificators:{
	# 	"<ModuleName>" : {
	#		result:[
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
def formatPoolBasedALRound(userquery, classifierasking, resultsForUserQuery):
	repo = {'repoName':userquery['name'], 'repoAPILink':userquery['api_url']}
	classificators = {}
	for cresult in resultsForUserQuery:
		classificators[cresult[0]] = {'result':formatProbabilities(cresult[1]), 'uncertainty':float(cresult[2])}
	returndata = {'repo':repo,'classifierAsking':classifierasking.getName(), 'classificators':classificators}
	return json.dumps(returndata)
	#return '{"repo":{"repoName": "rName", "repoAPILink":""}, "classifierAsking":"Neural Network1","classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}'
	# EXAMPLE
	# {
	# "repo":{repoName: "repoName","repoAPILink":""},	
	# "classifierAsking":"Neural Network1",
	# "classificators":{
	# 	"<ModuleName>" : {
	#		"result":[
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
	classificators = {}
	for result in results:
		classificators[result[0]] = {'result':formatClassificatorAccuracy(result[1][1]), 'yield':result[1][0]}
	returndata = {'classificators':classificators}
	return json.dumps(returndata)	
	#return '[ { "name" : "blub", "yield" : 0.84, "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}, { "name" : "blub2", "yield" : 0.84, "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}]'
	# EXAMPLE
	# {classificators:{
	# 	"<ModuleName>" : {
	#		result:[
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


def formatSingleClassificationTest(classifier,result):
	classificators = {}
	classificators[classifier.getName()] = {'result':formatClassificatorAccuracy(result[1]), 'yield':float(result[0])}
	returndata = {'classificators':classificators}
	return json.dumps(returndata)
	#return '[ { "name" : "blub", "yield" : 0.84, "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}]'

	# EXAMPLE
	# {classificators:{
	# 	"<ModuleName>" : {
	#		result:[
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
		savePointsOutput[savePoint[0]] = {'result':formatClassificatorAccuracy(savePoint[1]), 'yield':savePoint[2]}
	returndata = {'savepoints': savePointsOutput}
	return json.dumps(returndata)
	#return '[ { "name" : "blub", "yield" : 0.84, "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}, { "name" : "blub2", "yield" : 0.84, "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}, { "name" : "blub3", "yield" : 0.84, "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}]'
	# EXAMPLE
	# {savepoints:{
	# 	"<filename>" : {
	#		result:[
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

#nehmen da ja jetzt stattdessen testSingleClassifier bzw format davon
#def formatClassifierLoaded(classifier):
#	return 'NotImplemented'
	# EXAMPLE
	# {classificators:{
	# 	"<ModuleName>" : {
	#		result:[
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

def formatClassificatorAccuracy(classificatoraccuracy):
	accuracies = []
	accuracies.append({'class':'DEV', 'val':float(classificatoraccuracy['DEV'])})
	accuracies.append({'class':'HW', 'val':float(classificatoraccuracy['HW'])})
	accuracies.append({'class':'EDU', 'val':float(classificatoraccuracy['EDU'])})
	accuracies.append({'class':'DOCS', 'val':float(classificatoraccuracy['DOCS'])})
	accuracies.append({'class':'WEB', 'val':float(classificatoraccuracy['WEB'])})
	accuracies.append({'class':'DATA', 'val':float(classificatoraccuracy['DATA'])})
	accuracies.append({'class':'OTHER', 'val':float(classificatoraccuracy['OTHER'])})
	return accuracies

def formatRepo(repo):
	repo = {'repoName':sample['name'], 'repoAPILink':sample[api_url]}
	return repo