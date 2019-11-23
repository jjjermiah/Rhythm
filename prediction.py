from tensorflow import keras
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Activation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
test1 = pd.read_csv("test1.csv", header=None)
model = keras.models.load_model("bigboy.h5")
predict = model.predict(test1)



classificationFull = [
    "Normal",
    "Atrial premature, Aberrant atrial premature, Nodal premature, Supra-ventricular premature",
    " Premature ventricular contraction, Ventricular escape",
    "Fusion of ventricular and normal",
    "Paced, Fusion of paced and normal, Unclassifiable",
    
]

classification = ["N", "S", "V", "F", "Q"]

mostLikely = max(predict[0])

print("The Patient is likley to have", mostLikely, "of", classificationFull[predict[0].index(max(predict[0]))])


#for i in range(len(predict[0])):
#    print("\n",predict[0][i])


#print(predict)
#print(model)
