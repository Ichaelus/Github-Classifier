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

# Initialize ClassifierCollection
classifiercollection = ClassifierCollection()
#Initialize ClassificationModules
print 'Getting DB Descriptions to be able to create vectorizer in nndescription'
descriptionCorpus = DC.getAllDescriptions()
print 'Getting DB Readmes to be able to create vectorizer in nndescription'
readmeCorpus = DC.getAllReadmes()
print 'Done getting DB Descriptions'
nndescription = nndescriptiononly(descriptionCorpus)
nnreadme = nnreadmeonly(readmeCorpus)
classifiercollection.addClassificationModuleWithLastSavePoint(nndescription)
classifiercollection.addClassificationModuleWithLastSavePoint(nnreadme)
# pass ClassifierCollection to Controller
homesetclassifiercollection(classifiercollection)


#Start Bottle
if __name__ == '__main__':
    webbrowser.open("http://localhost:8080/")
    rootApp.merge(homebottle)
    rootApp.run(debug=True)
