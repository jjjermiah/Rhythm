from tensorflow import keras
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Activation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tkinter import *
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



root = Tk()


label_00 = Label(root, text="Luke Edward", bg="green", fg="black", font='Helvetica 24 bold')
label_01 = Label(root, text="Diagnosis:", font='Helvetica 18 bold')
label_01_value = Label(root, text=classificationFull[indexValue], font='Helvetica 20 bold')


label_00.grid(row=0)
label_01.grid(row=1)


label_01_value.grid(row=1, column=1)



for i in range(len(predict[0])):
    percent = str(predict[0][i]*100)
    label_i = Label(root, text=classificationFull[i], font='Helvetica 18')
    label_i_value = Label(root, text=percent[:-10]+"%", font='Helvetica 18')
    label_i.grid(row=i+2)
    label_i_value.grid(row=i+2, column=1)


root.mainloop()

