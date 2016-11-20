#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import Bottle, route, run, static_file


homebottle = Bottle()

@homebottle.get('/')
def home():
    return static_file("index.html", root="View", mimetype='text/html')

@homebottle.get('/bootstrap/js/<filename:re:.*\.js>')
def getBS(filename):
    return static_file(filename, root="View/bootstrap/js", mimetype='text/javascript')

@homebottle.get('/scripts/<filename:re:.*\.js>')
def getScript(filename):
	return static_file(filename, root="View/scripts", mimetype='text/javascript')

@homebottle.get('/bootstrap/css/<filename:re:.*\.css>')
def getBSC(filename):
	return static_file(filename, root="View/bootstrap/css", mimetype='text/css')

@homebottle.get('/css/<filename:re:.*\.css>')
def getCSS(filename):
	return static_file(filename, root="View/css", mimetype='text/css')

@homebottle.get('/fonts/<filename:re:.*\.woff>')
def getf(filename):
	return static_file(filename, root="View/fonts", mimetype='application/x-font-woff')

@homebottle.get('/fonts/<filename:re:.*\.woff2>')
def getf2(filename):
	return static_file(filename, root="View/fonts", mimetype='application/x-font-woff2')

@homebottle.get('/fonts/<filename:re:.*\.ttf>')
def getf3(filename):
	return static_file(filename, root="View/fonts", mimetype='application/x-font-ttf')

@homebottle.get('/bootstrap/fonts/<filename:re:.*\.woff>')
def getBSf(filename):
	return static_file(filename, root="View/bootstrap/fonts", mimetype='application/x-font-woff')

@homebottle.get('/bootstrap/fonts/<filename:re:.*\.woff2>')
def getBSf2(filename):
	return static_file(filename, root="View/bootstrap/fonts", mimetype='application/x-font-woff2')

@homebottle.get('/bootstrap/fonts/<filename:re:.*\.ttf>')
def getBSf3(filename):
	return static_file(filename, root="View/bootstrap/fonts", mimetype='application/x-font-ttf')

@homebottle.get('/post/<key>')
def api(key):
	if (key == "click"):
		return "Click event called"
	elif(key == "test"):
		return "backend connected!"
	else:
		return "API call for: " + key






