#!/usr/bin/env python
# -*- coding: utf-8 -*-
import demjson
import ClassificationModules.ClassificationModule

def ConvertClassifierCollectionToJSON(ClassifierCollection):
    # Return a list of classificator objects, containing the following attributes:
		# name: string, 
		# description:  string, 
		# yield: float [0-1], 
		# active: boolean,
		# result: []
		classificators = []
		for c in ClassifierCollection:
			accuracy = c.getAccuracy()
			result = []
			result.append({'class':'DEV', 'val':accuracy['DEV']})
			result.append({'class':'HW', 'val':accuracy['HW']})
			result.append({'class':'EDU', 'val':accuracy['EDU']})
			result.append({'class':'DOCS', 'val':accuracy['DOCS']})
			result.append({'class':'WEB', 'val':accuracy['WEB']})
			result.append({'class':'DATA', 'val':accuracy['DATA']})
			result.append({'class':'OTHER', 'val':accuracy['OTHER']})
			c = {'name':c.getName(), 'description':c.getDescription(), 'yield':c.getYield(), 'active':c.isMuteClassificationModule(), 'result':result}
			classificators.append(c)
		returndata = {'classificators': classificators}
		#return demjson.encode(returndata)
		return '{"classificators": [{"name":"Neural network1","description":"A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.","yield":0.81,"active":true,"result":[{"class":"DEV","val":0.0},{"class":"HW","val":0.0},{"class":"EDU","val":0.0},{"class":"DOCS","val":0.0},{"class":"WEB","val":0.0},{"class":"DATA","val":0.0},{"class":"OTHER","val":0.0}]},{"name":"Neural network2","description":"A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.","yield":0.55,"active":false,"result":[{"class":"DEV","val":0.0},{"class":"HW","val":0.0},{"class":"EDU","val":0.0},{"class":"DOCS","val":0.0},{"class":"WEB","val":0.0},{"class":"DATA","val":0.0},{"class":"OTHER","val":0.0}]},{"name":"Neural network3","description":"A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.","yield":0.90,"active":true,"result":[{"class":"DEV","val":0.0},{"class":"HW","val":0.0},{"class":"EDU","val":0.0},{"class":"DOCS","val":0.0},{"class":"WEB","val":0.0},{"class":"DATA","val":0.0},{"class":"OTHER","val":0.0}]}]}'
			# EXAMPLE
			# {
			#	classificators: [{
			#	name: "Neural network",
			#	description: "A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.",
			#	yield: "81",
			#	active: true,
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
			#	]
			#}]
#}
def getFormulas():
	return '["Entropy-Based", "Least Confident", "Margin-Sampling"]'


def formatSinglePrediction(result):
	# Response: a result vector for every classificator. Format:
			# [cid1: vector1, ..., cidN: vectorN] where cid = classificator ID, vector:
			# [{class: className, val: classificationResult}, ... ]
	return '{"repoName": "rName", "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}'
	# Updated Example
	# {
	# 	"repoName": "repoName",
	# 	"classificatorResults":[{
	# 	"<ModuleName>" : {
	#		{class: "DEV", val : 0.04},
	#		{class: "HW", val : 0.13},
	#		...
	# 	}]
	# 	}
	# 

def formatStreamBasedALRound(result):
	#result = (sample, unsure, SemiSupervisedL, SemiSupervisedLabel, results)
	return '{"repo": {"repoName": "rName", "repoAPILink":""}, "classifiersUnsure":"true","semisupervised":{"SemiSupervisedSureEnough":"false","SemiSupervisedLabel":"None"} ,"classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}'
	# {
	# 	"repo":{repoName: "repoName","repoAPILink":""},
	#	"classifiersUnsure":"true",
	#	"semisupervised":{"SemiSupervisedSureEnough":"false","SemiSupervisedLabel":"None"}
	# 	"classificatorResults":[{
	# 	"<ModuleName>" : {
	#		{class: "DEV", val : 0.04},
	#		{class: "HW", val : 0.13},
	#		...
	# 	}]
	# 	}
	# 

def formatPoolBasedALRound(result):
	#result = userquery, classifierasking, propabilitiesForUserQuery
	return '{"repo":{"repoName": "rName", "repoAPILink":""}, "classifierAsking":"Neural Network1","classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}'
	# {
	# 	"repo":{repoName: "repoName","repoAPILink":""},
	#	"classifierAsking":"Neural Network1",
	# 	"classificatorResults":[{
	#		{class: "DEV", val : 0.04},
	#		{class: "HW", val : 0.13},
	#		...
	# 	}]
	# 	}
	# 


def formatMultipleClassificationTests(result):
	'[ { "name" : "blub", "yield" : 0.84, "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}, { "name" : "blub2", "yield" : 0.84, "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}]'

#'[ 
	#{ 
		#"name" : "NeruralNetwork1", 
		#"yield" : 0.84, 
	# 	"classificatorResults":[{
	# 	"<ModuleName>" : {
		#	{"class": "DEV", "val" : 0.04},
		#	{"class": "HW", val : 0.13}, 
		#	{class: "EDU", val : 0.11},
		#	{class: "DOCS", val : 0.24}, 
		#	{class: "WEB", val : 0.59},
		#	{class: "DATA", val : 0.02},
		#	{class: "OTHER", val : 0.04}
		# }
		#]
	#},
	#{ 
		#"name" : "NeruralNetwork2", 
		#"yield" : 0.84, 
		#"yield" : 
		#[
			#{class: "DEV", val : 0.04},
			#{class: "HW", val : 0.13}, 
			#{class: "EDU", val : 0.11},
			#{class: "DOCS", val : 0.24}, 
			#{class: "WEB", val : 0.59},
			#{class: "DATA", val : 0.02},
			#{class: "OTHER", val : 0.04}
		#]
	#}
#]'

def formatSingleClassificationTest(result):
		return '[ { "name" : "blub", "yield" : 0.84, "classificatorResults" : {"Neural network1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network2":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"Neural network3":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}]'

#{ 
	#"name" : "neural network1", 
	#"yield" : 0.84, 
	# 	"classificatorResults":[{
	# 	"<ModuleName>" : {
	#	{"class": "DEV", "val" : 0.04},
	#	{"class": "HW", "val" : 0.13}, 
	#	{"class": "EDU", "val" : 0.11},
	#	{"class": "DOCS", "val" : 0.24}, 
	#	{"class": "WEB", "val" : 0.59},
	#	{"class": "DATA", "val" : 0.02},
	#	{"class": "OTHER", "val" : 0.04}
	#	}
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