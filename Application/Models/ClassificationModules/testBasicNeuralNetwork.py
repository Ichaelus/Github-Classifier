from basicneuralnetwork import basicneuralnetwork

text_corpus = ["This is a test", "Why is this a test", "This a test"]
test_sample = {"description":"Why", "class":"EDU"}

train_samples = [{"description":"Test is a", 'class':"DEV"}, {"description":"Why", 'class':"HW"}]

bn = basicneuralnetwork(text_corpus)
bn.train(train_samples)
bn.trainOnSample(test_sample)
bn.resetAllTraining()
print(bn.predictLabel(test_sample))
print(bn.predictLabelAndProbability(test_sample))