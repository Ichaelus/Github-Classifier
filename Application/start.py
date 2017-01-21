#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################################
# Initialization and startup file #
###################################

def packageMissing(name):
    raise ImportError('Dependency \''+name+'\' has not been found. Please refer to the installation manual.')

import time
try:
    from bottle import Bottle
except ImportError:
    packageMissing("Bottle")
serverUsed = ""
try:
    import cherrypy
    serverUsed = "cherrypy"
    cherrypy.response.timeout = 14400000
    cherrypy.config.update({'response.timeout': 14400000})
    cherrypy.engine.timeout_monitor.unsubscribe()
except ImportError:
    try: # Fallback for MacOS
        import paste
        serverUsed = "paste"
    except ImportError:
        packageMissing("paste")

import webbrowser
from Controllers.HomeController import homebottle, homesetclassifiercollection
from Models.ClassifierCollection import ClassifierCollection
#from Models.ClassificationModules.nndescriptiononly import nndescriptiononly
#from Models.ClassificationModules.lrdescriptiononly import lrdescriptiononly
#from Models.ClassificationModules.nnreadmeonly import nnreadmeonly
#from Models.ClassificationModules.lrreadmeonly import lrreadmeonly
#from Models.ClassificationModules.readmeonlyrandomforest import readmeonlyrandomforest
#from Models.ClassificationModules.multinomialnbreadmeonly import multinomialnbreadmeonly
#from Models.ClassificationModules.multinomialnbdescriptiononly import multinomialnbdescriptiononly
#from Models.ClassificationModules.bernoullinbreadmeonly import bernoullinbreadmeonly
#from Models.ClassificationModules.bernoullinbdescriptiononly import bernoullinbdescriptiononly
#from Models.ClassificationModules.nnmetaonly import nnmetaonly
#from Models.ClassificationModules.metaonlyrandomforest import metaonlyrandomforest
#from Models.ClassificationModules.metaonlysvc import metaonlysvc
#from Models.ClassificationModules.metaonlyadaboost import metaonlyadaboost
#from Models.ClassificationModules.reponamelstm import reponamelstm
#from Models.ClassificationModules.readmelstm import readmelstm
#from Models.ClassificationModules.nnall import nnall
#from Models.ClassificationModules.knnreadmeonly import knnreadmeonly
#from Models.ClassificationModules.svcfilenamesonly import filenamesonlysvc
#from Models.ClassificationModules.lrstacking import lrstacking
from Models.ClassificationModules.svmall import svmall
#from Models.ClassificationModules.rfall import allrandomforest
#from Models.ClassificationModules.gbrtmetaonly import gbrtmetaonly
#from Models.ClassificationModules.gbrtreadmeonly import gbrtreadmeonly
#from Models.ClassificationModules.gbrtfilesandfolders import gbrtfilesandfolders
#from Models.ClassificationModules.gbrtdescriptionmeta import gbrtdescriptionmeta
#from Models.ClassificationModules.svmreadmemeta import svmreadmemeta
#from Models.ClassificationModules.allbernoullinb import allbernoullinb
#from Models.ClassificationModules.allmultinomialnb import allmultinomialnb
#from Models.ClassificationModules.averageensemble import averageensemble
#from Models.ClassificationModules.nnstacking import nnstacking
#from Models.ClassificationModules.lrstackingmeta import lrstackingmeta
#from Models.ClassificationModules.foldernameslstm import foldernameslstm
#from Models.ClassificationModules.descriptionfoldersreponamelstm import descriptionfoldersreponamelstm
#from Models.ClassificationModules.descriptionlstm import descriptionlstm
#from Models.ClassificationModules.descriptionreponamelstm import descriptionreponamelstm

import Models.DatabaseCommunication as DC

print("Starting application..")

rootApp = Bottle()

# Initialize ClassifierCollection
classifiercollection = ClassifierCollection()

print 'Getting DB Data to be able to create vectorizers for classifiers that need it'
descriptionCorpus, readmeCorpus, filenameCorpus, filetypeCorpus, foldernameCorpus = DC.getCorpi()


#Initialize Classifiers
print 'Creating and adding Classifiers to Classifier Collection:'

# First load all classifiers which don't need other classifiers as parameter

loadedClassifiers = [] # Keep track, which classifiers have be loaded or such attempt has been made

classifiers = {}

#classifiers['filenamesonlysvc'] = filenamesonlysvc(filenameCorpus)
#classifiers['nnmetaonly'] = nnmetaonly()
#classifiers['metaonlysvc'] = metaonlysvc()
#classifiers['metaonlyadaboost'] = metaonlyadaboost()
#classifiers['metaonlyrandomforest'] = metaonlyrandomforest()
#classifiers['gbrtreadmeonly'] = gbrtreadmeonly(readmeCorpus)
#classifiers['gbrtfilesandfolders'] = gbrtfilesandfolders(filenameCorpus, foldernameCorpus)
#classifiers['gbrtmetaonly'] = gbrtmetaonly()
#classifiers['gbrtdescriptionmeta'] = gbrtdescriptionmeta(descriptionCorpus)
#classifiers['svmreadmemeta'] = svmreadmemeta(readmeCorpus)
#
#classifiers['descriptionlstm'] = descriptionlstm()
#classifiers['descriptionfoldersreponamelstm'] = descriptionfoldersreponamelstm()
#classifiers['foldernameslstm'] = foldernameslstm()
#classifiers['reponamelstm'] = reponamelstm()
#classifiers['readmelstm'] = readmelstm()
#classifiers['descriptionreponamelstm'] = descriptionreponamelstm()


for classifier in classifiers:
    loaded_classifier = classifiers[classifier].loadClassificationModuleSavePoint(filename="lastused")
    if loaded_classifier is not None:
        classifiers[classifier] = loaded_classifier
    loadedClassifiers.append(classifier)

# Now all classifiers should have been loaded from last savepoint, if available
# Use these loaded classifiers by giving them to specific ensemble-Models

#classifiers['nnall'] = nnall(readmeCorpus + descriptionCorpus, filetypeCorpus, filenameCorpus, foldernameCorpus)
classifiers['svmall'] = svmall(readmeCorpus + descriptionCorpus, filetypeCorpus, filenameCorpus, foldernameCorpus)
#classifiers['allrandomforest'] = allrandomforest(readmeCorpus + descriptionCorpus, filetypeCorpus, filenameCorpus, foldernameCorpus)
#classifiers['allmultinomialnb'] = allmultinomialnb(readmeCorpus + descriptionCorpus, filetypeCorpus, filenameCorpus, foldernameCorpus)
#classifiers['allbernoullinb'] = allbernoullinb(readmeCorpus + descriptionCorpus, filetypeCorpus, filenameCorpus, foldernameCorpus)


for classifier in classifiers:
    if classifier not in loadedClassifiers:
        loaded_classifier = classifiers[classifier].loadClassificationModuleSavePoint(filename="lastused")
        if loaded_classifier is not None:
            classifiers[classifier] = loaded_classifier
        loadedClassifiers.append(classifier)
        

#classifiers['lrstacking'] = lrstacking([classifiers['nnall'], classifiers['metaonlyrandomforest'], classifiers['svmall'], classifiers['metaonlysvc'], classifiers['allrandomforest'], classifiers['reponamelstm'], classifiers['gbrtdescriptionmeta']])
#classifiers['averageensemble'] = averageensemble([classifiers['nnall'], classifiers['metaonlyrandomforest'], classifiers['svmall'], classifiers['metaonlysvc'], classifiers['allrandomforest'], classifiers['reponamelstm'], classifiers['gbrtdescriptionmeta']])
#classifiers['nnstacking'] = nnstacking([classifiers['nnall'], classifiers['metaonlyrandomforest'], classifiers['svmall'], classifiers['metaonlysvc'], classifiers['allrandomforest'], classifiers['reponamelstm'], classifiers['gbrtdescriptionmeta']])
#classifiers['lrstackingmeta'] = lrstackingmeta([classifiers['nnall'], classifiers['metaonlyrandomforest'], classifiers['svmall'], classifiers['metaonlysvc'], classifiers['allrandomforest'], classifiers['reponamelstm'], classifiers['gbrtdescriptionmeta']])
# Finally load all meta-models such as lrstacking

for classifier in classifiers:
    if classifier not in loadedClassifiers:
        loaded_classifier = classifiers[classifier].loadClassificationModuleSavePoint(filename="lastused")
        if loaded_classifier is not None:
            classifiers[classifier] = loaded_classifier


#print 'Loading last checkpoint for classifiers if available:'
for c in classifiers:
    classifiercollection.addClassificationModule(classifiers[c])

# Pass ClassifierCollection to Controller
homesetclassifiercollection(classifiercollection)

# Wait a bit so website doesnt get called before it's ready
time.sleep(3)

print 'Done. Starting Bottle...'
#Start Bottle

if __name__ == '__main__':
    webbrowser.open("http://localhost:8080/")
    rootApp.merge(homebottle)
    rootApp.run(server=serverUsed, debug=True)
