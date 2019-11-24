from tensorflow import keras
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Activation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

myFile = pd.read_csv("datafile.csv", header=None)
model = keras.models.load_model("bigboy.h5")
predict = model.predict(myFile)

classificationFull = [
    "Normal",
    "Premature atrial contraction",
    " Premature ventricular contraction or Ventricular escape",
    "ventricular fibrillation",
    "Bradyarrhythmias",
    
]

#classification = ["N", "S", "V", "F", "Q"]

mostLikely = max(predict[0])
for i in range(len(predict[0])):
    if mostLikely == predict[0][i]:
        indexValue = i

percentage = mostLikely*100
print(percentage)
print(indexValue)
print("\nThe Patient is likley to have {:8.6f}% chance of {}.\n".format(percentage,classificationFull[indexValue]))