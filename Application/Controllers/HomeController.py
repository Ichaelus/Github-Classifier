#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import Bottle, route, run, static_file, request
import os


abspath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Views')

homebottle = Bottle()


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
		return '["e=mc²", "Abra kadabra"]'

	elif(key == "poolSize"):
		# Return the amount of unlabeled samples
		return "875"

	elif(key == "classificators"):
		# Return a list of classificator objects, containing the following attributes:
		# id: int, 
		# name: string, 
		# description: 
		# string, 
		# accuracy: int [0-100], 
		# active: boolean,
		# result: []
		return '[{"id":1,"name":"Neural network","description":"A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.","accuracy":"81","active":true,"result":[{"class":"DEV","val":0.0},{"class":"HW","val":0.0},{"class":"EDU","val":0.0},{"class":"DOCS","val":0.0},{"class":"WEB","val":0.0},{"class":"DATA","val":0.0},{"class":"OTHER","val":0.0}]},{"id":2,"name":"Neural network","description":"A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.","accuracy":"55","active":false,"result":[{"class":"DEV","val":0.0},{"class":"HW","val":0.0},{"class":"EDU","val":0.0},{"class":"DOCS","val":0.0},{"class":"WEB","val":0.0},{"class":"DATA","val":0.0},{"class":"OTHER","val":0.0}]},{"id":2,"name":"Neural network","description":"A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.","accuracy":"90","active":true,"result":[{"class":"DEV","val":0.0},{"class":"HW","val":0.0},{"class":"EDU","val":0.0},{"class":"DOCS","val":0.0},{"class":"WEB","val":0.0},{"class":"DATA","val":0.0},{"class":"OTHER","val":0.0}]}]'
			# EXAMPLE
			# [{
			#	id: 1,
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
			
	elif(key == "doSingleStep"):
		# Perform a single step based on the current stateData
		# if(queries["mode"] == "stream"):
		
		# Response: a result vector for every classificator. Format:
		# [cid1: vector1, ..., cidN: vectorN] where cid = classificator ID, vector:
		# [{class: className, val: classificationResult}, ... ]
		return '{"0":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"1":[{"class":"DEV","val":0.94},{"class":"HW","val":0.03},{"class":"EDU","val":0.01},{"class":"DOCS","val":0.04},{"class":"WEB","val":0.09},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}],"2":[{"class":"DEV","val":0.04},{"class":"HW","val":0.13},{"class":"EDU","val":0.11},{"class":"DOCS","val":0.24},{"class":"WEB","val":0.59},{"class":"DATA","val":0.02},{"class":"OTHER","val":0.04}]}'

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




