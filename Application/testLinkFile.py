#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
from bottle import Bottle
import webbrowser
from Controllers.HomeController import homebottle, homesetclassifiercollection
from Models.ClassifierCollection import ClassifierCollection
from Models.ClassificationModules.nndescriptiononly import nndescriptiononly
from Models.ClassificationModules.lrdescriptiononly import lrdescriptiononly
from Models.ClassificationModules.nnreadmeonly import nnreadmeonly
from Models.ClassificationModules.lrreadmeonly import lrreadmeonly
from Models.ClassificationModules.readmeonlyrandomforest import readmeonlyrandomforest
from Models.ClassificationModules.multinomialnbreadmeonly import multinomialnbreadmeonly
from Models.ClassificationModules.multinomialnbdescriptiononly import multinomialnbdescriptiononly
from Models.ClassificationModules.bernoullinbreadmeonly import bernoullinbreadmeonly
from Models.ClassificationModules.bernoullinbdescriptiononly import bernoullinbdescriptiononly
from Models.ClassificationModules.nnmetaonly import nnmetaonly
from Models.ClassificationModules.metaonlyrandomforest import metaonlyrandomforest
from Models.ClassificationModules.metaonlysvc import metaonlysvc
from Models.ClassificationModules.metaonlyadaboost import metaonlyadaboost
from Models.ClassificationModules.reponamelstm import reponamelstm
from Models.ClassificationModules.readmelstm import readmelstm
from Models.ClassificationModules.nnall import nnall
from Models.ClassificationModules.knnreadmeonly import knnreadmeonly
from Models.ClassificationModules.svcfilenamesonly import filenamesonlysvc
from Models.ClassificationModules.lrstacking import lrstacking
import Models.DatabaseCommunication as DC
import Models.JSONCommunication



rootApp = Bottle()

# Initialize ClassifierCollection
classifiercollection = ClassifierCollection()

#Initialize ClassificationModules
print 'Getting DB Data to be able to create vectorizers for classifiers that need it'
#descriptionCorpus = DC.getAllDescriptions()
#readmeCorpus = DC.getAllReadmes()
#filenameCorpus = DC.getAllFilenames()
descriptionCorpus, readmeCorpus, filenameCorpus, filetypeCorpus, foldernameCorpus = DC.getCorpi()

#Initialize Classifiers
print 'Creating and adding Classifiers to Classifier Collection:'
classifiers = []
#classifiers.append(nndescriptiononly(descriptionCorpus))
#classifiers.append(lrdescriptiononly(descriptionCorpus))
#classifiers.append(nnreadmeonly(readmeCorpus))
#classifiers.append(lrreadmeonly(readmeCorpus))
#classifiers.append(readmeonlyrandomforest(readmeCorpus))
#classifiers.append(knnreadmeonly(readmeCorpus))
#classifiers.append(multinomialnbdescriptiononly(descriptionCorpus))
#classifiers.append(multinomialnbreadmeonly(readmeCorpus))
#classifiers.append(bernoullinbdescriptiononly(descriptionCorpus))
#classifiers.append(bernoullinbreadmeonly(readmeCorpus))
classifiers.append(nnall(readmeCorpus + descriptionCorpus, filetypeCorpus, foldernameCorpus))
#classifiers.append(filenamesonlysvc(filenameCorpus))
#classifiers.append(nnmetaonly())
#classifiers.append(metaonlyrandomforest())
#classifiers.append(metaonlysvc())
#classifiers.append(metaonlyadaboost())
#classifiers.append(reponamelstm())
#classifiers.append(lrstacking([nnmetaonly(), metaonlyadaboost(), reponamelstm(), nnall(readmeCorpus + descriptionCorpus, filetypeCorpus, foldernameCorpus)]))
#classifiers.append(readmelstm())

print 'Loading last checkpoint for classifiers if available:'
for c in classifiers:
	classifiercollection.addClassificationModuleWithLastSavePoint(c)

# Pass ClassifierCollection to Controller
homesetclassifiercollection(classifiercollection)

# Wait a bit so website doesnt get called before it's ready
time.sleep(3)

#if __name__ == '__main__':
    #webbrowser.open("http://localhost:8080/")
    #rootApp.merge(homebottle)
    #rootApp.run(server='paste', debug=True)
if len(sys.argv) <= 1:
    sys.exit()
try:
    linkFile = open(sys.argv[1], "r")
    resultFile = open('classification_result.txt', "w")
    data, result = None, None
    classes = ['DEV', 'HW', 'EDU', 'DOCS', 'WEB', 'DATA', 'OTHER']
    for line in linkFile:
        print line.rstrip()
        data = DC.getInformationsForRepo(line.rstrip())
        prediction = classifiers[0].predictLabelAndProbability(data)
        resultFile.write(line.rstrip() + ' ' + classes[prediction[0]] + '\n')
    linkFile.close()
    resultFile.close()
except IOError:
    print "Der Kommandozeilenparameter war keine Datei", sys.exc_info()[0]
