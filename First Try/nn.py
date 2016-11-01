# -*- coding: utf-8 -*-
"""
Created on Tuesday Nov 1 01:59:00 2016

@author: andreas
"""

import utilities
from utilities import *
from keras.models import Sequential
from keras.layers import Dense, Activation



# Get raw text + labels
texts, labels, label_names = get_data()

# trainingsdaten werden in eingabedaten (vektoren) umgewandelt
# features ist dann matrix bestehend aus den einzelnen vektoren
features = vectorize_text(texts)

# x sind die eingabematrizen, y sind die vektoren in denen die ergebnisse stehen
x_train, x_test, y_train, y_test = split_train_test(features, labels, ratio=0.7, shuffle=False)

# One-Hot-Encoding needed for Neural Net Output
y_train = one_hot_encoding(y_train)
y_test = one_hot_encoding(y_test)

# Struktur des Netzes
model = Sequential()
input_size = x_train.shape[1]
model.add(Dense(input_size, input_dim=input_size))
model.add(Activation('relu'))
model.add(Dense(input_size * 3))
model.add(Activation('relu'))
# Output Layer, one neuron per class
model.add(Dense(7))
# Softmax zum Normalisieren der Werte, damit Wert des Neurons WSK in % angibt
model.add(Activation('softmax'))

model.compile(metrics=['accuracy'], optimizer='adam', loss='categorical_crossentropy')

# Train for 10 epochs
model.fit(x_train, y_train, nb_epoch=10, shuffle=True)

#variablen zum analysieren der ergebnisse
succ = 0
total = 0
dev_count = 0

# Test other samples
pred = model.predict(x_test)
for i in xrange(len(x_test)):
    if np.argmax(y_test[i]) != label_names.index('DEV'):
        if np.argmax(pred[i]) == np.argmax(y_test[i]):
            succ = succ + 1
        total = total + 1
    if np.argmax(pred[i]) == 0:
        dev_count = dev_count + 1
succ = succ / float(total)

print "Ratio assumed dev/ all classes", float(dev_count) / len(x_test)

print "Result without dev:", succ
acc = model.evaluate(x_test, y_test, verbose=0)
print "Result with dev: ", acc[1]

