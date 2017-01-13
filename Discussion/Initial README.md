# Github Classifier

## Features

* Projektstruktur + (Ordner)Bezeichnung
* Readme + Short Description
* Dateiname
* Dateityp
* Author Organization (z.B. University of..)
* "Namespaces"
  * Markante Wörter je nach Klasse
  * Relativ zur Readme Länge
  * Initiale Bewertung, falls Wahrscheinlichkeit > x% direkte Klassifikation
  * Ansonsten Entscheidungsfindung durch SVM bzw. Klassenspezifischen Merkmalen
* Programmiersprachen
  
## Wie wählt man Samples aus?

* GitHub Top e.g. 4000-5000 
* Auswertung durch [Mechanical turk](https://www.mturk.com/)
* Liste aller Repositories ab Id:x https://api.github.com/repositories?since=<x>
  * Auswahl an Repos mit Watch + Star + Fork > 100 (e.g.)

## Mögliche Classifier

* Naive Bayes, SVM
  * Libaries: Sklearn
* Linear Classifier
  * Logistic Regression
  * Libraries: Tensorflow, Sklearn
* Neuronales Netz 
  * RNN (LSTM)
  * Convolutional Network (https://goo.gl/nfzeFz)
  * Libraries: Tensorflow, Keras, Caffe 
* Semi-Supervised Learning
  * Beispiel: https://github.com/tmadl/semisup-learn

## Textrepräsentation
* Bag of Words (https://en.wikipedia.org/wiki/Bag-of-words_model)
* Tf-Idf (https://de.wikipedia.org/wiki/Tf-idf-Ma%C3%9F)
* Word2Vec (http://sebastianruder.com/word-embeddings-1/)
* Doc2Vec (https://linanqiu.github.io/2015/10/07/word2vec-sentiment/)
* Feature Hashing (https://en.wikipedia.org/wiki/Feature_hashing)
* Libraries:
  * http://scikit-learn.org/stable/modules/feature_extraction.html
  * (Gensim für Word2Vec, Doc2Vec) https://rare-technologies.com/doc2vec-tutorial/

## Tools
* Lime: Explaining the predictions of any machine learning classifier (https://github.com/marcotcr/lime)
