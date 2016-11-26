from Controllers.HomeController import homebottle, homesetclassifiercollection
from Models.ClassifierCollection import ClassifierCollection
from Models.ClassificationModules.basicneuralnetwork import basicneuralnetwork
import Models.DatabaseCommunication as DC


classifiercollection = ClassifierCollection()
homesetclassifiercollection(classifiercollection)

descriptionCorcus = DC.getAllDescriptions()
bnn = basicneuralnetwork(7, descriptionCorcus)

classifiercollection.addClassificationModule(bnn)

classifiercollection.doStreamBasedALRound('entropy')