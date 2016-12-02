#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import Bottle
import webbrowser
from Controllers.HomeController import homebottle, homesetclassifiercollection
from Models.ClassifierCollection import ClassifierCollection
from Models.ClassificationModules.nndescriptiononly import nndescriptiononly
from Models.ClassificationModules.nnreadmeonly import nnreadmeonly
import Models.DatabaseCommunication as DC

print("Starting application..")

rootApp = Bottle()

# Should we create the ClassifierCollection here once and then pass it to the other controllers?
# Have no idea at the moment if that´s the best way to do it in our case
classifiercollection = ClassifierCollection()
homesetclassifiercollection(classifiercollection)
print 'Getting DB Descriptions to be able to create vectorizer in nndescription'
descriptionCorpus = DC.getAllDescriptions()
print 'Getting DB Readmes to be able to create vectorizer in nndescription'
readmeCorpus = DC.getAllReadmes()
print 'Done getting DB Descriptions'
nndescription = nndescriptiononly(descriptionCorpus)
nnreadme = nnreadmeonly(readmeCorpus)
classifiercollection.addClassificationModule(nndescription)
classifiercollection.addClassificationModule(nnreadme)
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
    rootApp.run(server='paste', debug=True)
