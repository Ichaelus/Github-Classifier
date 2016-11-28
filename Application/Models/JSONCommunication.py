#!/usr/bin/env python
# -*- coding: utf-8 -*-
import demjson
import json
import ClassificationModules.ClassificationModule

def ConvertClassifierCollectionToJSON(classificationModules):
	classificators = []
	classificatornames = []
	accuracies = []
	for c in classificationModules:
		accuracy = c.getAccuracy()
		accuracies.append(accuracy)
		classificatornames.append(c.getName())
		c = {'name':c.getName(), 'description':c.getDescription(), 'yield':c.getYield(), 'active':c.isMuteClassificationModule()}
		classificators.append(c)
	classificatorResults = formatClassificatorAccuracyResult(classificatornames, accuracies)
	returndata = {'classificators': classificators, 'classificatorResults': classificatorResults}
	#return demjson.encode(returndata)
	return '{"classificators": [{"name":"Neural network1","description":"A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.","yield":0.81,"active":true,"result":[{"class":"DEV","val":0.0},{"class":"HW","val":0.0},{"class":"EDU","val":0.0},{"class":"DOCS","val":0.0},{"class":"WEB","val":0.0},{"class":"DATA","val":0.0},{"class":"OTHER","val":0.0}]},{"name":"Neural network2","description":"A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.","yield":0.55,"active":false,"result":[{"class":"DEV","val":0.0},{"class":"HW","val":0.0},{"class":"EDU","val":0.0},{"class":"DOCS","val":0.0},{"class":"WEB","val":0.0},{"class":"DATA","val":0.0},{"class":"OTHER","val":0.0}]},{"name":"Neural network3","description":"A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.","yield":0.90,"active":true,"result":[{"class":"DEV","val":0.0},{"class":"HW","val":0.0},{"class":"EDU","val":0.0},{"class":"DOCS","val":0.0},{"class":"WEB","val":0.0},{"class":"DATA","val":0.0},{"class":"OTHER","val":0.0}]}]}'
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
	#		active: true,
	#		uncertainty: 0.5	
	#	}}
	#}

def getFormulas():
	return '["Entropy-Based", "Least Confident", "Margin-Sampling"]'


def formatSinglePrediction(data, result):
	repoName = data['name']
	classificatorResults = formatClassificatorResults(result)
	returndata = {'repoName':repoName, 'classificatorResults':classificatorResults}
	#returnjson = demjson.encode(returndata)
	returnjson = json.dump(returndata)
	return returnjson
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
	semisupervised = {'SemiSupervisedSureEnough': SemiSupervisedL, 'SemiSupervisedLabel': SemiSupervisedLabel}
	classificatorResults = formatClassificatorResults(results)
	returndata = {'repo':repo, 'classifiersUnsure':unsure, 'semisupervised':semisupervised, 'classificatorResults':classificatorResults
	}
	print str(returndata)
	returnjson = demjson.encode(returndata)

	return '{"repo": {"repoName": "rName", "repoAPILink":""}, "classifiersUnsure":"true","semisupervised":{"SemiSupervisedSureEnough":"false","SemiSupervisedLabel":"None"} ,"classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}'
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
	#	}}
	#}

#wollen wir hier von allen classifiern die uncertainties zum ausgewählten sample angeben?
def formatPoolBasedALRound(userquery, classifierasking, propabilitiesForUserQuery):
	repo = {'repoName':sample['name'], 'repoAPILink':sample[api_url]}
	classificatorResults = formatClassificatorResults(propabilitiesForUserQuery)
	returndata = {'repo':repo,'classifierAsking':classifierasking.getName(), 'classificatorResults':classificatorResults}
	returnjson = demjson.encode(returndata)
	#return returndata
	return '{"repo":{"repoName": "rName", "repoAPILink":""}, "classifierAsking":"Neural Network1","classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}'
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
	returndata = []
	for result in results:
		returndata.append(formatSingleClassificationTest(result))
	returnjson = demjson.encode(returndata)
	#return returndata	
	return '[ { "name" : "blub", "yield" : 0.84, "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}, { "name" : "blub2", "yield" : 0.84, "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}]'
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


def formatSingleClassificationTest(result):
		return '[ { "name" : "blub", "yield" : 0.84, "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}]'

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
def formatSavePoints(savePointNames):
	#example: 1 safepoint only
	return '[ { "name" : "blub", "yield" : 0.84, "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}, { "name" : "blub2", "yield" : 0.84, "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}, { "name" : "blub3", "yield" : 0.84, "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}]'
	# EXAMPLE
	# {safepoints:{
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

#Hilfsunktionen für oben
def formatClassificatorResults(results):
	classificatorResults = {}
	for cresult in results:
		cname = cresult[0]
		cprobabilities = []
		cprobabilities.append({'class':'DEV', 'val': float(cresult[1][1])})
		cprobabilities.append({'class':'HW', 'val': float(cresult[1][2])})
		cprobabilities.append({'class':'EDU', 'val': float(cresult[1][3])})
		cprobabilities.append({'class':'DOCS', 'val': float(cresult[1][4])})
		cprobabilities.append({'class':'WEB', 'val': float(cresult[1][5])})
		cprobabilities.append({'class':'DATA', 'val': float(cresult[1][6])})
		cprobabilities.append({'class':'OTHER', 'val': float(cresult[1][7])})
		classificatorResults[cname] = cprobabilities
	return classificatorResults

def formatClassificatorAccuracyResult(classificatornames, accuracies):
	classificatorResults = []
	for i in xrange(len(classificatornames)):
		result = []
		result.append({'class':'DEV', 'val':float(accuracies[i]['DEV'])})
		result.append({'class':'HW', 'val':float(accuracies[i]['HW'])})
		result.append({'class':'EDU', 'val':float(accuracies[i]['EDU'])})
		result.append({'class':'DOCS', 'val':float(accuracies[i]['DOCS'])})
		result.append({'class':'WEB', 'val':float(accuracies[i]['WEB'])})
		result.append({'class':'DATA', 'val':float(accuracies[i]['DATA'])})
		result.append({'class':'OTHER', 'val':float(accuracies[i]['OTHER'])})
		classificatorResults.append({classificatornames[i] : result})
	return classificatorResults

def formatRepo(repo):
	repo = {'repoName':sample['name'], 'repoAPILink':sample[api_url]}
	return repo