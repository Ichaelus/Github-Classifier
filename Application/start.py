#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
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
from Models.ClassificationModules.svmall import svmall
from Models.ClassificationModules.lrstacking import lrstacking
import Models.DatabaseCommunication as DC

print("Starting application..")

rootApp = Bottle()

# Initialize ClassifierCollection
classifiercollection = ClassifierCollection()

#Initialize ClassificationModules
print 'Getting DB Data to be able to create vectorizers for classifiers that need it'
descriptionCorpus = DC.getAllDescriptions()
readmeCorpus = DC.getAllReadmes()
filenameCorpus = DC.getAllFilenames()

#Initialize Classifiers
print 'Creating and adding Classifiers to Classifier Collection:'


nndescription = nndescriptiononly(descriptionCorpus)
lrdescription = lrdescriptiononly(descriptionCorpus)
nnreadme = nnreadmeonly(readmeCorpus)
lrreadme = lrreadmeonly(readmeCorpus)
rfreadme = readmeonlyrandomforest(readmeCorpus)
knnreadme = knnreadmeonly(readmeCorpus)
mnbdescription = multinomialnbdescriptiononly(descriptionCorpus)
mnbreadme = multinomialnbreadmeonly(readmeCorpus)
bnbdescription = bernoullinbdescriptiononly(descriptionCorpus)
bnbreadme = bernoullinbreadmeonly(readmeCorpus)
nnmeta = nnmetaonly()
rfmeta = metaonlyrandomforest()
#lstmreadme = readmelstm()

abmeta = metaonlyadaboost()
svcmeta = metaonlysvc()
svcfilenames = filenamesonlysvc(filenameCorpus)
nnall = nnall(readmeCorpus + descriptionCorpus)
allsvm = svmall(readmeCorpus + descriptionCorpus)
lstmname = reponamelstm()

stackinglr = lrstacking([nnall, lstmname, allsvm, svcmeta, svcfilenames, nnreadme, nndescription, rfreadme, mnbreadme, rfmeta, abmeta])

print 'Loading last checkpoint for classifiers if available:'

"""
classifiercollection.addClassificationModuleWithLastSavePoint(nndescription)
classifiercollection.addClassificationModuleWithLastSavePoint(nnreadme)
classifiercollection.addClassificationModuleWithLastSavePoint(lrreadme)
classifiercollection.addClassificationModuleWithLastSavePoint(rfreadme)
classifiercollection.addClassificationModuleWithLastSavePoint(lrdescription)
classifiercollection.addClassificationModuleWithLastSavePoint(mnbdescription)
classifiercollection.addClassificationModuleWithLastSavePoint(mnbreadme)
classifiercollection.addClassificationModuleWithLastSavePoint(bnbdescription)
classifiercollection.addClassificationModuleWithLastSavePoint(bnbreadme)
classifiercollection.addClassificationModuleWithLastSavePoint(nnmeta)
classifiercollection.addClassificationModuleWithLastSavePoint(rfmeta)
classifiercollection.addClassificationModuleWithLastSavePoint(svcmeta)
classifiercollection.addClassificationModuleWithLastSavePoint(abmeta)
#classifiercollection.addClassificationModuleWithLastSavePoint(lstmreadme)
classifiercollection.addClassificationModuleWithLastSavePoint(knnreadme)
classifiercollection.addClassificationModuleWithLastSavePoint(svcfilenames)
"""
classifiercollection.addClassificationModuleWithLastSavePoint(nnall)
classifiercollection.addClassificationModuleWithLastSavePoint(allsvm)
classifiercollection.addClassificationModuleWithLastSavePoint(lstmname)
classifiercollection.addClassificationModuleWithLastSavePoint(stackinglr)

# Pass ClassifierCollection to Controller
homesetclassifiercollection(classifiercollection)

# Wait a bit so website doesnt get called before it's ready
time.sleep(3)

print 'Done. Starting Bottle...'
#Start Bottle
if __name__ == '__main__':
    webbrowser.open("http://localhost:8080/")
    rootApp.merge(homebottle)
    rootApp.run(server='paste', debug=True)
