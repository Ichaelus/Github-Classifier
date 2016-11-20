#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ClassifierCollection:
    """A class to deal with multiple Classification Modules"""
    
    classificationmodules = []
    #def __init__(self):
        # We need to test here later what´s the most recently used and safed collection and load it
        #self.classificationmodules = ...
    
    @classmethod
    def getClassificationModulesJSON (self):
        """Return some basic informations about each Classification Module."""
        return 'NotImplemented'
    @classmethod
    def addClassificationModule(self, module):
        self.classificationmodules.append(module)

    
