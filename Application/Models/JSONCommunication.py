#!/usr/bin/env python
# -*- coding: utf-8 -*-

def ConvertClassifierCollectionToJSON(ClassifierCollection):
    # Return a list of classificator objects, containing the following attributes:
		# name: string, 
		# description: 
		# string, 
		# accuracy: int [0-100], 
		# active: boolean,
		# result: []
		return '{"classificators": [{"name":"Neural network","description":"A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.","accuracy":"81","active":true,"result":[{"class":"DEV","val":0.0},{"class":"HW","val":0.0},{"class":"EDU","val":0.0},{"class":"DOCS","val":0.0},{"class":"WEB","val":0.0},{"class":"DATA","val":0.0},{"class":"OTHER","val":0.0}]},{"name":"Neural network","description":"A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.","accuracy":"55","active":false,"result":[{"class":"DEV","val":0.0},{"class":"HW","val":0.0},{"class":"EDU","val":0.0},{"class":"DOCS","val":0.0},{"class":"WEB","val":0.0},{"class":"DATA","val":0.0},{"class":"OTHER","val":0.0}]},{"name":"Neural network","description":"A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.","accuracy":"90","active":true,"result":[{"class":"DEV","val":0.0},{"class":"HW","val":0.0},{"class":"EDU","val":0.0},{"class":"DOCS","val":0.0},{"class":"WEB","val":0.0},{"class":"DATA","val":0.0},{"class":"OTHER","val":0.0}]}]}'
			# EXAMPLE
			# {
			# 	repoName: "RepoName",
			#	classificators: [{
			#	name: "Neural network",
			#	description: "A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.",
			#	accuracy: "81",
			#	active: true,
			#	result: [
			#		{class: "DEV", val : 0.04},
			#		{class: "HW", val : 0.13},
			#		{class: "EDU", val : 0.11},
			#		{class: "DOCS", val : 0.24},
			#		{class: "WEB", val : 0.59},
			#		{class: "DATA", val : 0.02},
			#		{class: "OTHER", val : 0.04}
			#	]
			#}]
			#}

def getFormulas():
	return '["Entropy-Based", "Least Confident", "Margin-Sampling"]'


def formatSinglePrediction(result):
	# Response: a result vector for every classificator. Format:
			# [cid1: vector1, ..., cidN: vectorN] where cid = classificator ID, vector:
			# [{class: className, val: classificationResult}, ... ]
	return '{"repoName": "rName", "classificatorResults" : {"0":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"2":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}'
	# Updated Example
	# {
	# 	"repoName": "repoName",
	# 	"classificatorResults":[{
	#		{class: "DEV", val : 0.04},
	#		{class: "HW", val : 0.13},
	#		...
	# 	}]
	# 	}
	# 

def formatPoolBasedALRound(result):
	#result = userquery, classifierasking, propabilitiesForUserQuery
	return '{{"repoName": "rName", "repoAPILink":""}, "classifierAsking":"NeuralNetwork","classificatorResults" : {"0":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"2":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}'
	# {
	# 	"repo":{repoName: "repoName","repoAPILink":""},
	#	"classifierAsking":"NeuralNetwork",
	# 	"classificatorResults":[{
	#		{class: "DEV", val : 0.04},
	#		{class: "HW", val : 0.13},
	#		...
	# 	}]
	# 	}
	# 

def formatStreamBasedALRound(result):
	#result = (sample, unsure, SemiSupervisedL, SemiSupervisedLabel, results)
	return '{{"repoName": "rName", "repoAPILink":""}, "classifiersUnsure":"true","semisupervised":{"SemiSupervisedSureEnough":"false","SemiSupervisedLabel":"None"} ,"classificatorResults" : {"0":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"2":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}}'
	# {
	# 	"repo":{repoName: "repoName","repoAPILink":""},
	#	"classifiersUnsure":"true",
	#	"semisupervised":{"SemiSupervisedSureEnough":"false","SemiSupervisedLabel":"None"}
	# 	"classificatorResults":[{
	#		{class: "DEV", val : 0.04},
	#		{class: "HW", val : 0.13},
	#		...
	# 	}]
	# 	}
	# 


def formatMultipleClassificationTests(result):
	'[ { "name" : "blub", "yield" : 0.84, "accuracy" : [{class: "DEV", val : 0.04},{class: "HW", val : 0.13}, {class: "EDU", val : 0.11},{class: "DOCS", val : 0.24}, {class: "WEB", val : 0.59},{class: "DATA", val : 0.02},{class: "OTHER", val : 0.04}]}, { "name" : "blub2", "yield" : 0.84, "accuracy" : [{class: "DEV", val : 0.04},{class: "HW", val : 0.13}, {class: "EDU", val : 0.11},{class: "DOCS", val : 0.24}, {class: "WEB", val : 0.59},{class: "DATA", val : 0.02},{class: "OTHER", val : 0.04}]}, { "name" : "blub3", "yield" : 0.84, "accuracy" : [{class: "DEV", val : 0.04},{class: "HW", val : 0.13}, {class: "EDU", val : 0.11},{class: "DOCS", val : 0.24}, {class: "WEB", val : 0.59},{class: "DATA", val : 0.02},{class: "OTHER", val : 0.04}]}]'

#'[ 
	#{ 
		#"name" : "NeruralNetwork1", 
		#"yield" : 0.84, 
		#"accuracy" : 
		#[
		#	{class: "DEV", val : 0.04},
		#	{class: "HW", val : 0.13}, 
		#	{class: "EDU", val : 0.11},
		#	{class: "DOCS", val : 0.24}, 
		#	{class: "WEB", val : 0.59},
		#	{class: "DATA", val : 0.02},
		#	{class: "OTHER", val : 0.04}
		#]
	#},
	#{ 
		#"name" : "NeruralNetwork2", 
		#"yield" : 0.84, 
		#"accuracy" : 
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
		return '[ { "name" : "blub", "yield" : 0.84, "accuracy" : [{class: "DEV", val : 0.04},{class: "HW", val : 0.13}, {class: "EDU", val : 0.11},{class: "DOCS", val : 0.24}, {class: "WEB", val : 0.59},{class: "DATA", val : 0.02},{class: "OTHER", val : 0.04}]}]'

#{ 
	#"name" : "neuralnetwork", 
	#"yield" : 0.84, 
	#"accuracy" : 
	#[
	#	{class: "DEV", val : 0.04},
	#	{class: "HW", val : 0.13}, 
	#	{class: "EDU", val : 0.11},
	#	{class: "DOCS", val : 0.24}, 
	#	{class: "WEB", val : 0.59},
	#	{class: "DATA", val : 0.02},
	#	{class: "OTHER", val : 0.04}
	#]
#}
def formatSavePoints(savePointNames):
	#example: 1 safepoint only
	return '[ { "name" : "blub", "yield" : 0.84, "accuracy" : [{class: "DEV", val : 0.04},{class: "HW", val : 0.13}, {class: "EDU", val : 0.11},{class: "DOCS", val : 0.24}, {class: "WEB", val : 0.59},{class: "DATA", val : 0.02},{class: "OTHER", val : 0.04}]}, { "name" : "blub2", "yield" : 0.84, "accuracy" : [{class: "DEV", val : 0.04},{class: "HW", val : 0.13}, {class: "EDU", val : 0.11},{class: "DOCS", val : 0.24}, {class: "WEB", val : 0.59},{class: "DATA", val : 0.02},{class: "OTHER", val : 0.04}]}, { "name" : "blub3", "yield" : 0.84, "accuracy" : [{class: "DEV", val : 0.04},{class: "HW", val : 0.13}, {class: "EDU", val : 0.11},{class: "DOCS", val : 0.24}, {class: "WEB", val : 0.59},{class: "DATA", val : 0.02},{class: "OTHER", val : 0.04}]}]'

#'[ 
	#{ 
		#"name" : "11.11.2011:11:11blub", 
		#"yield" : 0.84, 
		#"accuracy" : 
		#[
		#	{class: "DEV", val : 0.04},
		#	{class: "HW", val : 0.13}, 
		#	{class: "EDU", val : 0.11},
		#	{class: "DOCS", val : 0.24}, 
		#	{class: "WEB", val : 0.59},
		#	{class: "DATA", val : 0.02},
		#	{class: "OTHER", val : 0.04}
		#]
	#},
	#{ 
		#"name" : "11.11.2011:11:11blub2", 
		#"yield" : 0.84, 
		#"accuracy" : 
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