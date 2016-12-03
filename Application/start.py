#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import Bottle
import webbrowser
from Controllers.HomeController import homebottle, homesetclassifiercollection
from Models.ClassifierCollection import ClassifierCollection
from Models.ClassificationModules.nndescriptiononly import nndescriptiononly
from Models.ClassificationModules.lrdescriptiononly import lrdescriptiononly
from Models.ClassificationModules.nnreadmeonly import nnreadmeonly
from Models.ClassificationModules.lrreadmeonly import lrreadmeonly
from Models.ClassificationModules.readmeonlyrandomforest import readmeonlyrandomforest
import Models.DatabaseCommunication as DC

print("Starting application..")

rootApp = Bottle()

# Initialize ClassifierCollection
classifiercollection = ClassifierCollection()
#Initialize ClassificationModules
print 'Getting DB Descriptions to be able to create vectorizer in nndescription'
descriptionCorpus = DC.getAllDescriptions()
print 'Getting DB Readmes to be able to create vectorizer in nndescription'
readmeCorpus = DC.getAllReadmes()
print 'Done getting DB Descriptions'
nndescription = nndescriptiononly(descriptionCorpus)
lrdescription = lrdescriptiononly(descriptionCorpus)
nnreadme = nnreadmeonly(readmeCorpus)
lrreadme = lrreadmeonly(readmeCorpus)
rfreadme = readmeonlyrandomforest(readmeCorpus)
classifiercollection.addClassificationModule(nndescription)
classifiercollection.addClassificationModule(nnreadme)
classifiercollection.addClassificationModule(lrreadme)
classifiercollection.addClassificationModule(rfreadme)
classifiercollection.addClassificationModule(lrdescription)
#on startup load last used version. also for testing loading
#ClassifierName = bnn.getName()
#try:
#    newModule = classifiercollection.getClassificationModule(ClassifierName).loadClassificationModuleSavePoint()
#    classifiercollection.setClassificationModule(ClassifierName, newModule)
#    print 'succesfully loaded old bnn-version: ' + str(newModule)
#except NameError as err:
#    raise err
classifiercollection.addClassificationModuleWithLastSavePoint(nndescription)
classifiercollection.addClassificationModuleWithLastSavePoint(nnreadme)
#initialize Accuracy and Yield for all ClassificationModules
#(pickle doesn´t seem to save class variables of abstract parent class)
classifiercollection.TestAllClassificationModules()
# pass ClassifierCollection to Controller
homesetclassifiercollection(classifiercollection)


#Start Bottle
if __name__ == '__main__':
    webbrowser.open("http://localhost:8080/")
    rootApp.merge(homebottle)
    rootApp.run(server='paste', debug=True)
