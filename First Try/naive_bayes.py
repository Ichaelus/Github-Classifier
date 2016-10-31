# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 11:58:08 2016

@author: andreas
"""

import utilities
from utilities import *



#hole data als dict
data = api_call()

#liste mit strings von den feature texten
texts = []
#die namen der klassen
label_names = []
#die klassen
labels = []

# im moment wird NUR die description verwendet, nicht die readme
whatIWant = 'description'

# vectorizer braucht liste von strings, hier wirds umgewandelt
for i in xrange(len(data)):
    if whatIWant == 'readme':
        #nur die readme ist anscheinend decoded
        text = text_from_base64(data[i][whatIWant])
    text = data[i][whatIWant]
    text = text.replace('\n', ' ')
    texts.append(text)
    label = data[i]['class']
    if label not in label_names:
        label_names.append(label)
    labels.append(label_names.index(label))


# trainingsdaten werden in eingabedaten (vektoren) umgewandelt
# features ist dann matrix bestehend aus den einzelnen vektoren
features = get_feature_vec(texts)
# x sind die eingabematrizen, y sind die vektoren in denen die ergebnisse stehen
x_train, x_test, y_train, y_test = split_train_test(features, labels, ratio=0.7)

# das trainieren mit den daten
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
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

print "Result without dev:", succ
print "Result with dev: ", clf.score(x_test, y_test)

