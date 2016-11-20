#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class ClassificationModule:
    __metaclass__ = ABCMeta

    description = "Doesnt have a description yet"

    @abstractmethod
    def foo(self):
        pass

    @classmethod
    def getdescription(self):
        return self.description
    