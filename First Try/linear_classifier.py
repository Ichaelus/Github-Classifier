# -*- coding: utf-8 -*-
"""
Created on Tuesday Nov 1 01:52:00 2016

@author: andreas
"""

import utilities
from utilities import *


# Get raw text + labels
texts, labels, label_names = get_data()

# trainingsdaten werden in eingabedaten (vektoren) umgewandelt
# features ist dann matrix bestehend aus den einzelnen vektoren
features = vectorize_text(texts)

# x sind die eingabematrizen, y sind die vektoren in denen die ergebnisse stehen
x_train, x_test, y_train, y_test = split_train_test(features, labels, ratio=0.7)

# das trainieren mit den daten
from sklearn.linear_model import SGDClassifier

clf = SGDClassifier()
clf.fit(x_train, y_train)

#variablen zum analysieren der ergebnisse
succ = 0
total = 0
dev_count = 0

#wir gehen testdaten durch und schaun wie sie eingeordnet werden
for i in xrange(len(x_test)):
    pred = clf.predict([x_test[i]])
    if y_test[i] != label_names.index('DEV'):
        if pred == y_test[i]:
            succ = succ + 1
        total = total + 1
    if pred == 0:
        dev_count = dev_count + 1
succ = succ / float(total)

print "Ratio assumed dev/ all classes", float(dev_count) / len(x_test)
print "Result without dev:", succ
print "Result with dev: ", clf.score(x_test, y_test)

