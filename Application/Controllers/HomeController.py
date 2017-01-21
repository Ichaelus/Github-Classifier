#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################
# GUI <-> Python Controller #
#############################

def packageMissing(name):
    raise ImportError('Dependency \''+name+'\' has not been found. Please refer to the installation manual.')

import os

try:
	from bottle import Bottle, route, run, static_file, request
except ImportError:
	packageMissing("bottle")

try:
    if os.name.lower() == "nt":
	    import cherrypy
	    cherrypy.response.timeout = 14400000
	    cherrypy.config.update({'response.timeout': 14400000})
	    cherrypy.engine.timeout_monitor.unsubscribe()
except ImportError:
	pass

import Models.ClassifierCollection
import Models.JSONCommunication as JS
import Models.DatabaseCommunication as DC

abspath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Views') # The default OS independent path
homebottle = Bottle()
CC = None # Classifier Collection

# Serve static files at given paths

def homesetclassifiercollection(classifiercollection):
	global CC
	CC = classifiercollection

@homebottle.get('/')
def home():
    return static_file("index.html", root = abspath, mimetype='text/html')

@homebottle.get('/<filename:re:.*\.html>')
def home_c(filename):
    return static_file(filename, root = abspath, mimetype='text/html')

@homebottle.get('/favicon.ico')
def home_fi():
    return static_file("favicon.ico", root = abspath, mimetype='image/x-icon')

@homebottle.get('/favicon.png')
def home_fp():
    return static_file("favicon.png", root = abspath, mimetype='image/png')

@homebottle.get('/loading.gif')
def home_loading():
    return static_file("loading.gif", root = abspath, mimetype='image/gif')

@homebottle.get('/images/<filename:re:.*\.jpg>')
def image(filename):
    return static_file(filename, root=os.path.join(abspath, "images"), mimetype='image/jpg')

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

@homebottle.get('/Documentation/<filename:re:.*\.jpg>')
def getDocumentationImage(filename):
	docsPath = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'), '../Documentation')
	return static_file(filename, root=docsPath, mimetype='image/jpg')

@homebottle.get('/Documentation/<filename:re:.*\.png>')
def getDocumentationPng(filename):
	docsPath = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'), '../Documentation')
	return static_file(filename, root=docsPath, mimetype='image/png')



@homebottle.get('/get/<key>')
def api(key):
	# Handle Frontend to Python requests

	if (key == "formulas"):
		# Return a string list of available uncertainty formulas
		return JS.getFormulas()

	elif(key == "poolSize"):
		# Return the amount of unlabeled samples
		return DC.getUnlabeledCount()

	elif(key == "classifiers"):
		# get classifiers
		classifiers = CC.getAllClassificationModules()
		return JS.ConvertClassifierCollectionToJSON(classifiers)

	elif(key == "doSingleStep"):
		# Perform a single step based on the current stateData
		if(getQueryValue("mode") == "stream"):
			sample, unsure, SemiSupervisedL, SemiSupervisedLabel, results = CC.doStreamBasedALRound(getQueryValue("formula"), getQueryValue("isSemiSupervised") == 'true')
			return JS.formatStreamBasedALRound(sample, unsure, SemiSupervisedL, SemiSupervisedLabel, results)

		elif(getQueryValue("mode") == "pool"):
			sample, classifierasking, propabilitiesForUserQuery = CC.doPoolBasedALRound(getQueryValue("formula"), getQueryValue("isSemiSupervised") == 'true')
			return JS.formatPoolBasedALRound(sample, classifierasking, propabilitiesForUserQuery)
		else:
			return "Invalid arguments"

	elif(key == "PredictSingleSample"):
		# Returns classifier prediction for a given `repoLink`
		data, result = None, None
		try:
			data, result = CC.PredictSingleSample(getQueryValue("repoLink"))
			return JS.formatSinglePrediction(data, result)
		except Exception as e:
			print e
			return JS.toJson({'error': str(e)})

	elif(key == "startTest"):
		# Runs the classifiers agains a predefined testset
		useExtendedTestSet = getQueryValue("useExtendedTestSet") == "true"
		result = CC.TestAllClassificationModules(useExtendedTestSet)
		return JS.formatMultipleClassificationTests(result)

	elif(key == "retrain"):
		# Retrains a single classifier identified by <name>
		ClassifierName = getQueryValue("name")
		useExtendedTestSet = getQueryValue("useExtendedTestSet") == "true"
		try:
			# Get data to train on
			train_data = DC.getTrainData()
			classifier = CC.getClassificationModule(ClassifierName)
			classifier.resetAllTraining()
			classifier.train(train_data)

			# Test classifier
			test_data = DC.getTestData(useExtendedTestSet)
			return JS.formatSingleClassificationTest(classifier, classifier.testModule(test_data))
		except Exception as e:
			print e
			return JS.toJson({'error': str(e)})

	elif(key == "retrainSemiSupervised"):
		# Retrains a single classifier identified by <name> including semi-supervised data
		ClassifierName = getQueryValue("name")
		useExtendedTestSet = getQueryValue("useExtendedTestSet") == "true"
		try:
			"""
			# Get data to train on
			train_data = DC.getSemiSupervisedData()
			classifier = CC.getClassificationModule(ClassifierName)
			classifier.resetAllTraining()
			classifier.train(train_data)

			# Test classifier
			test_data = DC.getTestData(useExtendedTestSet)
			return classifier.testModule(train_data)
			"""
			return "NotImplemented"
		except:
			return "The classifier "+ClassifierName+" has been retrained with semi-supervised data."

	elif(key == "save"):
		# Saves a classifier snapshot to disk
		ClassifierName = getQueryValue("name")
		#try:
		classifier = CC.getClassificationModule(ClassifierName)
		classifier.saveModule()
		return "The classifier "+ClassifierName+" has been saved."
		#except:
		#	return "Error while saving classifier."

	elif(key == "load"):
		# Loads and retests a classifier snapshot
		ClassifierName = getQueryValue("name")
		useExtendedTestSet = getQueryValue("useExtendedTestSet") == "true"
		#try:
		newModule = CC.getClassificationModule(ClassifierName).loadClassificationModuleSavePoint(getQueryValue("savepoint"))
		CC.setClassificationModule(ClassifierName, newModule)
		test_data = DC.getTestData(useExtendedTestSet)
		return JS.formatSingleClassificationTest(newModule, newModule.testModule(test_data))
		#except:
		#	return('{"Error": "Error loading classifier"}')

	elif(key == "savePoints"):
		# Returns a list of savepoint filenames for classifier <name>
		ClassifierName = getQueryValue("name")
		try:
			savePoints = CC.getClassificationModule(ClassifierName).getSavePointsForClassificationModules()
			return JS.formatSavePoints(savePoints)
		except NameError as err:
			return('Name error')

	elif(key == "ALclassification"):
		# Save user classification <label> for a repository <api_url>
		if("api_url" == ""):
			return "API url is empty"
		data = DC.moveRepoFromToClassifyToTrain(getQueryValue("api_url"), getQueryValue("label"))
		if(getQueryValue("trainInstantly") == "true"):
			CC.ALTrainInstantlyAllClassificationModules(data)

	elif(key == "mute"):
		# Mutes a module <name>
		try:
			CC.getClassificationModule(getQueryValue("name")).muteClassificationModule()
			return "success"
		except NameError as err:
			return('Module not found')


	elif(key == "unmute"):
		# Unmutes a module <name>
		try:
			CC.getClassificationModule(getQueryValue("name")).unmuteClassificationModule()
			return "success"
		except NameError as err:
			return('Module not found')

	elif(key == "matrix"):
		# Returns the confusion matrix for module <name>
		try:
			return JS.formatxfusionMatrix(CC.getClassificationModule(getQueryValue("name")).getConfusionMatrix())
		except NameError as err:
			return('Module not found')

	elif(key == "stats"):
		# Get database statistics for <table>
		if(getQueryValue("string_attrs") == "true"):
			return JS.formatStats(DC.getStats(getQueryValue("table"), "string"))
		else:
			return JS.formatStats(DC.getStats(getQueryValue("table"), "numerical"))
			
	elif(key == "distributionArray"):
		# Returns the class distribution for the table <table>. Flag for using extended set or not
		useExtendedTestSet = getQueryValue("useExtendedTestSet") == "true"
		return JS.toJson(DC.getDistributionArray(getQueryValue("table"), useExtendedTestSet))

	elif(key == "documentationNames"):
		# Returns a list of .md documentation files
		docsPath = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'), '../Documentation')
		docfiles = [f for f in os.listdir(docsPath) if os.path.isfile(os.path.join(docsPath, f)) and f.endswith(".md") and f.lower() != 'readme.md']
		return JS.toJson(docfiles)

	elif(key == "getAPICalls"):
		# Returns the amount of API calls burned during the last hour
		return JS.toJson(DC.getAPICalls())

	else :
		return "API call for: " + key

def getQueryValue(q):
	# Returns a query <q> value passed to /get/ 
	queries = request.query.decode()
	if(q in queries):
		return queries[q]
	else:
		raise NameError('Query not set')
