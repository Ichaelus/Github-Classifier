from Controllers.HomeController import homebottle, homesetclassifiercollection
from Models.ClassifierCollection import ClassifierCollection
from Models.ClassificationModules.basicneuralnetwork import basicneuralnetwork
import Models.DatabaseCommunication as DC


classifiercollection = ClassifierCollection()
homesetclassifiercollection(classifiercollection)

descriptionCorcus = DC.getAllDescriptions()
bnn = basicneuralnetwork(descriptionCorcus)

classifiercollection.addClassificationModule(bnn)

print(classifiercollection.doStreamBasedALRound('Entropy-Based'))