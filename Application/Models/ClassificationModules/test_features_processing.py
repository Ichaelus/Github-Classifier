from DatabaseCommunication import getLabeledData
from FeatureProcessing import getVectorsFromData

import random


data = getLabeledData()
f, l, ln = getVectorsFromData(data)

print(f[random.randint(0, len(f))])