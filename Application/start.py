#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import Bottle
import webbrowser
from Controller.HomeController import homebottle
from Model.ClassifierCollection import ClassifierCollection
from Model.basicneuralnetwork import basicneuralnetwork

rootApp = Bottle()

# Should we create the ClassifierCollection here once and then pass it to the other controllers?
# Have no idea at the moment if that´s the best way to do it in our case
classifiercollection = ClassifierCollection()

#testing stuff
bnn = basicneuralnetwork()
classifiercollection.addClassificationModule(bnn)
print bnn.getdescription()
print classifiercollection.getClassificationModulesJSON()


if __name__ == '__main__':
    webbrowser.open("http://localhost:8080/")
    rootApp.merge(homebottle)
    rootApp.run(debug=True)