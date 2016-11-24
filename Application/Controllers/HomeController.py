#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import Bottle, route, run, static_file, request
import os
import Models.ClassifierCollection
import Models.JSONCommunication
import Models.DatabaseCommunication


abspath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Views')

homebottle = Bottle()
homeclassifiercollection = None

def homesetclassifiercollection(classifiercollection):
	global homeclassifiercollection
	homeclassifiercollection = classifiercollection

@homebottle.get('/')
def home():
    return static_file("index.html", root = abspath, mimetype='text/html')

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


@homebottle.get('/get/<key>')
def api(key):
	# Handle frontend to backend requests
	queries = request.query.decode()

	if (key == "formulas"):
		# Return a string list of available uncertainty formulas
		return Models.JSONCommunication.getFormulas()

	elif(key == "poolSize"):
		# Return the amount of unlabeled samples
		return Models.DatabaseCommunication.getUnlabeledCount()

	elif(key == "classificators"):
		# get classificators
		classificators = homeclassifiercollection.getAllClassificationModules()
		return Models.JSONCommunication.ConvertClassifierCollectionToJSON(classificators)
	elif(key == "doSingleStep"):
		# Perform a single step based on the current stateData
		# if(queries["mode"] == "stream"):
		result = homeclassifiercollection.doStreamBasedALRound('Entropy-Based')
		return Model.JSONCommunication.formatStreamBasedALRound(result)
		

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




