#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import Bottle, route, run, static_file, request
import os
import Models.ClassifierCollection
import Models.JSONCommunication
import Models.DatabaseCommunication as DC

abspath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Views')

homebottle = Bottle()
homeclassifiercollection = None

def homesetclassifiercollection(classifiercollection):
	global homeclassifiercollection
	homeclassifiercollection = classifiercollection

@homebottle.get('/')
def home():
    return static_file("index.html", root = abspath, mimetype='text/html')

@homebottle.get('/user_classification.html')
def home_c():
    return static_file("user_classification.html", root = abspath, mimetype='text/html')

@homebottle.get('/favicon.ico')
def home_fi():
    return static_file("favicon.ico", root = abspath, mimetype='image/x-icon')

@homebottle.get('/favicon.png')
def home_fp():
    return static_file("favicon.png", root = abspath, mimetype='image/png')

@homebottle.get('/loading.gif')
def home_loading():
    return static_file("loading.gif", root = abspath, mimetype='image/gif')

@homebottle.get('/images/facial_expressions/<filename:re:.*\.jpg>')
def facial_expressions(filename):
    return static_file(filename, root=os.path.join(os.path.join(abspath, "images"), "facial_expressions"), mimetype='image/jpg')

@homebottle.get('/scripts/<filename:re:.*\.js>')
def getScript(filename):
	return static_file(filename, root=os.path.join(abspath, "scripts"), mimetype='text/javascript')

@homebottle.get('/css/<filename:re:.*\.css>')
def getCSS(filename):
	return static_file(filename, root = os.path.join(abspath, "css"), mimetype='text/css')

@homebottle.get('/fonts/<filename:re:.*\.woff>')
def getf(filename):
	return static_file(filename, root = os.path.join(abspath, "fonts"), mimetype='application/x-font-woff')

@homebottle.get('/fonts/<filename:re:.*\.woff2>')
def getf2(filename):
	return static_file(filename, root = os.path.join(abspath, "fonts"), mimetype='application/x-font-woff2')

@homebottle.get('/fonts/<filename:re:.*\.ttf>')
def getf3(filename):
	return static_file(filename, root = os.path.join(abspath, "fonts"), mimetype='application/x-font-ttf')

@homebottle.get('/bootstrap/js/<filename:re:.*\.js>')
def getBS(filename):
    return static_file(filename, root=os.path.join(os.path.join(abspath, "bootstrap"), "js"), mimetype='text/javascript')

@homebottle.get('/bootstrap/css/<filename:re:.*\.css>')
def getBSC(filename):
	return static_file(filename, root=os.path.join(os.path.join(abspath, "bootstrap"), "css"), mimetype='text/css')
	
@homebottle.get('/bootstrap/fonts/<filename:re:.*\.woff>')
def getBSf(filename):
	return static_file(filename, root=os.path.join(os.path.join(abspath, "bootstrap"), "fonts"), mimetype='application/x-font-woff')

@homebottle.get('/bootstrap/fonts/<filename:re:.*\.woff2>')
def getBSf2(filename):
	return static_file(filename, root=os.path.join(os.path.join(abspath, "bootstrap"), "fonts"), mimetype='application/x-font-woff2')

@homebottle.get('/bootstrap/fonts/<filename:re:.*\.ttf>')
def getBSf3(filename):
	return static_file(filename, root=os.path.join(os.path.join(abspath, "bootstrap"), "fonts"), mimetype='application/x-font-ttf')

@homebottle.get('/docs/<filename:re:.*\.md>')
def getDocumentation(filename):
	docsPath = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'), '../Documentation')
	return static_file(filename, root=docsPath, mimetype='text/plain')

@homebottle.get('/get/<key>')
def api(key):
	# Handle frontend to backend requests

	if (key == "formulas"):
		# Return a string list of available uncertainty formulas
		return Models.JSONCommunication.getFormulas()

	elif(key == "poolSize"):
		# Return the amount of unlabeled samples
		return DC.getUnlabeledCount()

	elif(key == "classifiers"):
		# get classifiers
		classifiers = homeclassifiercollection.getAllClassificationModules()
		return Models.JSONCommunication.ConvertClassifierCollectionToJSON(classifiers)

	elif(key == "doSingleStep"):
		# Perform a single step based on the current stateData
		if(getQueryValue("mode") == "stream"):
			sample, unsure, SemiSupervisedL, SemiSupervisedLabel, results = homeclassifiercollection.doStreamBasedALRound(getQueryValue("formula"), getQueryValue("isSemiSupervised") == 'true')
			return Models.JSONCommunication.formatStreamBasedALRound(sample, unsure, SemiSupervisedL, SemiSupervisedLabel, results)

		elif(getQueryValue("mode") == "pool"):
			sample, classifierasking, propabilitiesForUserQuery = homeclassifiercollection.doPoolBasedALRound(getQueryValue("formula"), getQueryValue("isSemiSupervised") == 'true')
			return Models.JSONCommunication.formatPoolBasedALRound(sample, classifierasking, propabilitiesForUserQuery)
		else:
			return "Invalid arguments"

	elif(key == "PredictSingleSample"):
		# Returns classifier prediction for a given `repoLink`
		data, result = None, None
		#try:
		data, result = homeclassifiercollection.PredictSingleSample(getQueryValue("repoLink"))
		#except Exception, e:
		#	print e
		#	return e
		return Models.JSONCommunication.formatSinglePrediction(data, result)

	elif(key == "startTest"):
		# Runs the classifiers agains a predefined testset
		result = homeclassifiercollection.TestAllClassificationModules()
		return Models.JSONCommunication.formatMultipleClassificationTests(result)

	elif(key == "retrain"):
		ClassifierName = getQueryValue("name")
		#try:
			# Get data to train on
		train_data = Models.DatabaseCommunication.getTrainData()
		classifier = homeclassifiercollection.getClassificationModule(ClassifierName)
		classifier.resetAllTraining()
		classifier.train(train_data)

		# Test classifier
		test_data = Models.DatabaseCommunication.getTestData()
		return Models.JSONCommunication.formatSingleClassificationTest(classifier, classifier.testModule(test_data))
		#except:
		#	return "The classifier "+ClassifierName+" has been retrained."

	elif(key == "retrainSemiSupervised"):
		ClassifierName = getQueryValue("name")
		try:
			"""
			# Get data to train on
			train_data = DC.getSemiSupervisedData()
			classifier = homeclassifiercollection.getClassificationModule(ClassifierName)
			classifier.resetAllTraining()
			classifier.train(train_data)

			# Test classifier
			test_data = DC.getTestData()
			return classifier.testModule(train_data)
			"""
			return "NotImplemented"
		except:
			return "The classifier "+ClassifierName+" has been retrained with semi-supervised data."

	elif(key == "save"):
		ClassifierName = getQueryValue("name")
		#try:
		classifier = homeclassifiercollection.getClassificationModule(ClassifierName)
		classifier.saveModule()
		return "The classifier "+ClassifierName+" has been saved."
		#except:
		#	return "Error while saving classifier."

	elif(key == "load"):
		ClassifierName = getQueryValue("name")
		#try:
		newModule = homeclassifiercollection.getClassificationModule(ClassifierName).loadClassificationModuleSavePoint(getQueryValue("savepoint"))
		homeclassifiercollection.setClassificationModule(ClassifierName, newModule)
		test_data = Models.DatabaseCommunication.getTestData()
		return Models.JSONCommunication.formatSingleClassificationTest(newModule, newModule.testModule(test_data))
		#except:
		#	return('{"Error": "Error loading classifier"}')

	elif(key == "savePoints"):
		ClassifierName = getQueryValue("name")
		try:
			savePoints = homeclassifiercollection.getClassificationModule(ClassifierName).getSavePointsForClassificationModules()
			return Models.JSONCommunication.formatSavePoints(savePoints)
		except NameError as err:
			return('Name error')

	elif(key == "ALclassification"):
		# Save user classification
		if("api_url" == ""):
			return "API url is empty"
		data = DC.moveRepoFromToClassifyToTrain(getQueryValue("api_url"), getQueryValue("label"))
		if(getQueryValue("trainInstantly") == "true"):
			homeclassifiercollection.ALTrainInstantlyAllClassificationModules(data)

	elif(key == "mute"):
		try:
			homeclassifiercollection.getClassificationModule(getQueryValue("name")).muteClassificationModule()
			return "success"
		except NameError as err:
			return('Module not found')


	elif(key == "unmute"):
		try:
			homeclassifiercollection.getClassificationModule(getQueryValue("name")).unmuteClassificationModule()
			return "success"
		except NameError as err:
			return('Module not found')

	elif(key == "matrix"):
		try:
			return Models.JSONCommunication.formatxfusionMatrix(homeclassifiercollection.getClassificationModule(getQueryValue("name")).getConfusionMatrix())
		except NameError as err:
			return('Module not found')

	elif(key == "stats"):
		if(getQueryValue("string_attrs") == "true"):
			return Models.JSONCommunication.formatStats(DC.getStats(getQueryValue("table"), "string"))
		else:
			return Models.JSONCommunication.formatStats(DC.getStats(getQueryValue("table"), "numerical"))
			
	elif(key == "distributionArray"):
		return Models.JSONCommunication.toJson(DC.getDistributionArray(getQueryValue("table")))

	elif(key == "documentationNames"):
		docsPath = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'), '../Documentation')
		docfiles = [f for f in os.listdir(docsPath) if os.path.isfile(os.path.join(docsPath, f)) and f.endswith(".md")]
		return Models.JSONCommunication.toJson(docfiles)

	else :
		return "API call for: " + key

@homebottle.post('/post/<key>')
def api(key):
	if (key == "click"):
		return "Click event called"
	elif(key == "test"):
		return "backend connected!"
	else:
		return "API call for: " + key

def getQueryValue(q):
	queries = request.query.decode()
	if(q in queries):
		return queries[q]
	else:
		raise NameError('Query not set')
