# -*- coding: utf-8 -*-
"""
Created on Tuesday Nov 1 01:59:00 2016

@author: andreas
"""

import utilities
from utilities import *
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation

def test_sentence(sentence):
    sentence = process_text(sentence)
    vec = vectorizer.transform([sentence]).toarray()
    print "Label", label_names[np.argmax(model.predict_proba(vec))]
    out = model.predict_proba(vec)[0]
    prob_dev = out[0]
    prob_not = out[1]
    print "Proba DEV: {0:.2f} Not DEV: {1:.2f}".format(prob_dev, prob_not)

# Constants
binary = True

print "Get and process data"
# Get raw text + labels
features, labels, label_names = get_data('readme', binary=binary)
features, labels = shuffle_data(features, labels)
#features = np.matrix(features)

print "Vectorize data"
# trainingsdaten werden in eingabedaten (vektoren) umgewandelt
# features ist dann matrix bestehend aus den einzelnen vektore
features, vectorizer = vectorize_text(features, max_features=2000)

# x sind die eingabematrizen, y sind die vektoren in denen die ergebnisse stehen
x_train, x_test, y_train, y_test = split_train_test(features, labels, ratio=0.9, shuffle=True)

print "Prepare one-hot-encoding"
# One-Hot-Encoding needed for Neural Net Output
y_train = one_hot_encoding(y_train)
y_test = one_hot_encoding(y_test)

print "Build model"
# Struktur des Netzes
model = Sequential()
input_size = x_train.shape[1]
model.add(Dense(input_size, input_dim=input_size))
model.add(Activation('relu'))
model.add(Dense(input_size * 3))
model.add(Activation('relu'))
# Output Layer, one neuron per class
if binary:
    model.add(Dense(2))
else:
    model.add(Dense(8))
# Softmax zum Normalisieren der Werte, damit Wert des Neurons WSK in % angibt
model.add(Activation('softmax'))

model.compile(metrics=['accuracy'], optimizer='adam', loss='categorical_crossentropy')

print "Train model"
# Train for 10 epochs
model.fit(x_train, y_train, nb_epoch=5, shuffle=True)

#variablen zum analysieren der ergebnisse
succ = 0
total = 0
dev_pred_count = 0
dev_count = 0

# Test other samples
pred = model.predict(x_test)
for i in xrange(len(x_test)):
    if np.argmax(y_test[i]) != label_names.index('DEV'):
        if np.argmax(pred[i]) == np.argmax(y_test[i]):
            succ = succ + 1
        total = total + 1
    if np.argmax(pred[i]) == 0:
        dev_pred_count += 1
    if np.argmax(y_test[i]) == 0:
        dev_count += 1
succ = succ / float(total)

print "Ratio assumed dev/ all classes", float(dev_pred_count) / len(x_test)
print "Ratio dev / all classes", float(dev_count) / len(y_test)
print "Result without dev:", succ
acc = model.evaluate(x_test, y_test, verbose=0)
print "Result with dev: ", acc[1]

