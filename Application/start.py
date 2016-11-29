#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import Bottle
import webbrowser
from Controllers.HomeController import homebottle, homesetclassifiercollection
from Models.ClassifierCollection import ClassifierCollection
from Models.ClassificationModules.basicneuralnetwork import basicneuralnetwork
import Models.DatabaseCommunication as DC

print("Starting application..")

rootApp = Bottle()

# Should we create the ClassifierCollection here once and then pass it to the other controllers?
# Have no idea at the moment if that´s the best way to do it in our case
classifiercollection = ClassifierCollection()
homesetclassifiercollection(classifiercollection)
print 'Getting DB Descriptions to be able to create vectorizer in basicneuralnetwork'
descriptionCorpus = DC.getAllDescriptions()
print 'Done getting DB Descriptions'
bnn = basicneuralnetwork(descriptionCorpus)
classifiercollection.addClassificationModule(bnn)
#on startup load last used version. also for testing loading
#ClassifierName = bnn.getName()
#try:
#    newModule = classifiercollection.getClassificationModule(ClassifierName).loadClassificationModuleSavePoint()
#    classifiercollection.setClassificationModule(ClassifierName, newModule)
#    print 'succesfully loaded old bnn-version: ' + str(newModule)
#except NameError as err:
#    raise err

if __name__ == '__main__':
    webbrowser.open("http://localhost:8080/")
    rootApp.merge(homebottle)
    rootApp.run(debug=True)
