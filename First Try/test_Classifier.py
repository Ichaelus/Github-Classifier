from Classifier import Classifier

classifier_types = ["nn", "svm", "nb", "lr"]


X = [[0, 0], [1, 0], [0, 1], [1, 1]]
Y = [0, 1, 1, 0]

for clf_type in classifier_types:

    clf = Classifier(clf_type=clf_type, input_size=2, output_size=2)
    print clf_type.upper()
    clf.train(X, Y, nb_epoch=1000)
    clf.evaluate(X, Y)

    for x in X:
        print("Interpreted {} as {}".format(x, clf.predict(x)))




