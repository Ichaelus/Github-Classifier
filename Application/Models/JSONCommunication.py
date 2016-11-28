#!/usr/bin/env python
# -*- coding: utf-8 -*-
import demjson
import ClassificationModules.ClassificationModule

def ConvertClassifierCollectionToJSON(classificationModules):
    # Return a list of classificator objects, containing the following attributes:
		# name: string, 
		# description:  string, 
		# yield: float [0-1], 
		# active: boolean,
		# result: []
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
			# {
			#	classificators: [{
				#	name: "Neural network",
				#	description: "A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.",
				#	yield: "81",
				#	active: true
			#	],
			# 	"classificatorResults":[{
			# 		"<ModuleName>" : {[
			#			{class: "DEV", val : 0.04},
			#			{class: "HW", val : 0.13},
			#			{class: "EDU", val : 0.11},
			#			{class: "DOCS", val : 0.24},
			#			{class: "WEB", val : 0.59},
			#			{class: "DATA", val : 0.02},
			#			{class: "OTHER", val : 0.04}
			#		]	
			#	}]
			#}

def getFormulas():
	return '["Entropy-Based", "Least Confident", "Margin-Sampling"]'


def formatSinglePrediction(data, result):
	# Response: a result vector for every classificator. Format:
			# [cid1: vector1, ..., cidN: vectorN] where cid = classificator ID, vector:
			# [{class: className, val: classificationResult}, ... ]
	repoName = data['name']
	classificatorResults = formatClassificatorResults(result)
	returndata = {'repoName':repoName, 'classificatorResults':classificatorResults}
	returnjson = demjson.encode(returndata)
	return returnjson
	#return '{"repoName": "rName", "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}'
	# Updated Example
	# {
	# 	"repoName": "repoName",
	# 	"classificatorResults":[{
		# 	"<ModuleName>" : [{
		#		{class: "DEV", val : 0.04},
		#		{class: "HW", val : 0.13},
		#		...
		#	]
		#}]
	# 	}
	# 

#hier fehlt noch die uncertainty von jedem classifier jeweils
def formatStreamBasedALRound(sample, unsure, SemiSupervisedL, SemiSupervisedLabel, results):
	repo = {'repoName':sample['name'], 'repoAPILink':sample['api_url']}
	semisupervised = {'SemiSupervisedSureEnough': SemiSupervisedL, 'SemiSupervisedLabel': SemiSupervisedLabel}
	classificatorResults = formatClassificatorResults(results)
	returndata = {'repo':repo, 'classifiersUnsure':unsure, 'semisupervised':semisupervised, 'classificatorResults':classificatorResults
	}
	returnjson = demjson.encode(returndata)
	return '{"repo": {"repoName": "rName", "repoAPILink":""}, "classifiersUnsure":"true","semisupervised":{"SemiSupervisedSureEnough":"false","SemiSupervisedLabel":"None"} ,"classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}'
	# {
	# 	"repo":{repoName: "repoName","repoAPILink":""},
	#	"classifiersUnsure":"true",
	#	"semisupervised":{"SemiSupervisedSureEnough":"false","SemiSupervisedLabel":"None"},
	# 	"classificatorResults":[{
		# 	"<ModuleName>" : [{
		#		{class: "DEV", val : 0.04},
		#		{class: "HW", val : 0.13},
		#		...
		#	]
		# }]
	# }
	# 

#wollen wir hier von allen classifiern die uncertainties zum ausgewählten sample angeben?
def formatPoolBasedALRound(userquery, classifierasking, propabilitiesForUserQuery):
	repo = {'repoName':sample['name'], 'repoAPILink':sample[api_url]}
	classificatorResults = formatClassificatorResults(propabilitiesForUserQuery)
	returndata = {'repo':repo,'classifierAsking':classifierasking.getName(), 'classificatorResults':classificatorResults}
	returnjson = demjson.encode(returndata)
	#return returndata
	return '{"repo":{"repoName": "rName", "repoAPILink":""}, "classifierAsking":"Neural Network1","classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}'
	# {
	# 	"repo":{repoName: "repoName","repoAPILink":""},
	#	"classifierAsking":"Neural Network1",
	# 	"classificatorResults":[{
	#		{class: "DEV", val : 0.04},
	#		{class: "HW", val : 0.13},
	#		...
	# 	}]
	# }

#falls wirs als array von formatSingleClassificationTest machen, ansonsten muss das wieder anders ausschaun
def formatMultipleClassificationTests(results):
	returndata = []
	for result in results:
		returndata.append(formatSingleClassificationTest(result))
	returnjson = demjson.encode(returndata)
	#return returndata	
	return '[ { "name" : "blub", "yield" : 0.84, "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}, { "name" : "blub2", "yield" : 0.84, "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}]'
			# EXAMPLE
			# {
			#	classificators: [{
				#	name: "Neural network",
				#	yield: "81",
			#	}],
			# 	"classificatorResults":[{
			# 	"<ModuleName>" : {
			#		{class: "DEV", val : 0.04},
			#		{class: "HW", val : 0.13},
			#		{class: "EDU", val : 0.11},
			#		{class: "DOCS", val : 0.24},
			#		{class: "WEB", val : 0.59},
			#		{class: "DATA", val : 0.02},
			#		{class: "OTHER", val : 0.04}
			#		
			#	}]
			#}


def formatSingleClassificationTest(result):
		return '[ { "name" : "blub", "yield" : 0.84, "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}]'

#{ 
	#"name" : "neural network1", 
	#"yield" : 0.84, 
	# "classificatorResults":[{
	# 	"<ModuleName>" : [{
		#	{"class": "DEV", "val" : 0.04},
		#	{"class": "HW", "val" : 0.13}, 
		#	{"class": "EDU", "val" : 0.11},
		#	{"class": "DOCS", "val" : 0.24}, 
		#	{"class": "WEB", "val" : 0.59},
		#	{"class": "DATA", "val" : 0.02},
		#	{"class": "OTHER", "val" : 0.04}
	#	}]
	#]
#}
def formatSavePoints(savePointNames):
	#example: 1 safepoint only
	return '[ { "name" : "blub", "yield" : 0.84, "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}, { "name" : "blub2", "yield" : 0.84, "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}, { "name" : "blub3", "yield" : 0.84, "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}]'

#'[ 
	#{ 
		#"name" : "11.11.2011:11:11blub", 
		#"yield" : 0.84, 
	# 	"classificatorResults":[{
	# 	"<ModuleName>" : {
		#	{"class": "DEV", "val" : 0.04},
		#	{class: "HW", "val" : 0.13}, 
		#	{class: "EDU", val : 0.11},
		#	{class: "DOCS", val : 0.24}, 
		#	{class: "WEB", val : 0.59},
		#	{class: "DATA", val : 0.02},
		#	{class: "OTHER", val : 0.04}
		#	}
		#]
	#},
	#{ 
		#"name" : "11.11.2011:11:11blub2", 
		#"yield" : 0.84, 
	# 	"classificatorResults":[{
	# 	"<ModuleName>" : {
			#{class: "DEV", val : 0.04},
			#{class: "HW", val : 0.13}, 
			#{class: "EDU", val : 0.11},
			#{class: "DOCS", val : 0.24}, 
			#{class: "WEB", val : 0.59},
			#{class: "DATA", val : 0.02},
			#{class: "OTHER", val : 0.04}
			#}
		#]
	#}
#]'

#Hilfsunktionen für oben
def formatClassificatorResults(results):
	classificatorResults = []
	for cresult in results:
		cname = cresult[0]
		cprobabilities = []
		cprobabilities.append({'class':'DEV', 'val':cresult[1]})
		cprobabilities.append({'class':'HW', 'val':cresult[2]})
		cprobabilities.append({'class':'EDU', 'val':cresult[3]})
		cprobabilities.append({'class':'DOCS', 'val':cresult[4]})
		cprobabilities.append({'class':'WEB', 'val':cresult[5]})
		cprobabilities.append({'class':'DATA', 'val':cresult[6]})
		cprobabilities.append({'class':'OTHER', 'val':cresult[7]})
		classificatorResults.append({cname : cprobabilities})
	return classificatorResults

def formatClassificatorAccuracyResult(classificatornames, accuracies):
	classificatorResults = []
	for i in xrange(len(classificatornames)):
		result = []
		result.append({'class':'DEV', 'val':accuracies[i]['DEV']})
		result.append({'class':'HW', 'val':accuracies[i]['HW']})
		result.append({'class':'EDU', 'val':accuracies[i]['EDU']})
		result.append({'class':'DOCS', 'val':accuracies[i]['DOCS']})
		result.append({'class':'WEB', 'val':accuracies[i]['WEB']})
		result.append({'class':'DATA', 'val':accuracies[i]['DATA']})
		result.append({'class':'OTHER', 'val':accuracies[i]['OTHER']})
		classificatorResults.append({classificatornames[i] : result})
	return classificatorResults

def formatRepo(repo):
	repo = {'repoName':sample['name'], 'repoAPILink':sample[api_url]}
	return repo