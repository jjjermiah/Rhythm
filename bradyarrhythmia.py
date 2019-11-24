import csv
import serial
from tensorflow import keras
import time
from twilio.rest import Client
import pandas as pd
from tkinter import *


try:
    arduino = serial.Serial("COM8", timeout=1, baudrate=9600)   # Try opening the port at a determined baud rate (bits per second)
except:
    print('Please check the port')


with open("test1.csv", "w") as new_file:
    csv_writer = csv.writer(new_file, lineterminator = ',')

    line_count = 0
    while True:
        rawdata = str(arduino.readline().strip())  # Receive data and append to the list
        line_count += 1
        if(line_count>2):
            def clean(L):  # L is a list
                temp = L[2:]
                temp = temp[:-1]
                return int(temp)/1024
            cleandata = clean(rawdata)
            csv_writer.writerow([cleandata])

        if(line_count>188):
            break

print("Recording Complete")


myFile = pd.read_csv("bradyarrythmia.csv", header=None)
model = keras.models.load_model("bigboy.h5")
predict = model.predict(myFile)

classificationFull = [
    "Normal",
    "Premature atrial contraction",
    " Premature ventricular contraction or Ventricular escape",
    "ventricular fibrillation",
    "Bradyarrhythmias",

]

# classification = ["N", "S", "V", "F", "Q"]
indexValue = 0
mostLikely = max(predict[0])
for i in range(len(predict[0])):
    if mostLikely == predict[0][i]:
        indexValue = i

percentage = mostLikely * 100
print(percentage)
#print(indexValue)
#print("\nThe Patient is likley to have {:8.6f}% chance of {}.\n".format(percentage, classificationFull[indexValue]))

if indexValue in [0]:
    print("Patient seems to have normal readings")

else:
    account_sid = ""
    assistant_sid = ""
    auth_token = ""

    client = Client(account_sid, auth_token)

    call = client.calls.create(
        to="6479780432",
        from_="+17347990482",
        url='',

    )

    message = client.messages.create(
        body='Hello caregiver, Your patient Luke Edward seems to be experiencing heart atrial fibrillation, please take necessary actions',
        from_='+17347990482',
        to='6479780432'
    )

    print(call.sid)
    print(message.sid)

root = Tk()

label_00 = Label(root, text="Luke Edward", bg="green", fg="black", font='Helvetica 24 bold')
label_01 = Label(root, text="Diagnosis:", font='Helvetica 18 bold')
label_01_value = Label(root, text=classificationFull[indexValue], font='Helvetica 20 bold')

label_00.grid(row=0)
label_01.grid(row=1)

label_01_value.grid(row=1, column=1)

for i in range(len(predict[0])):
    print(predict[0][i])
    percent = str(predict[0][i] * 100)
    print(percent)

    label_i = Label(root, text=classificationFull[i], font='Helvetica 18')
    label_i_value = Label(root, text=percent[:-10] + "%", font='Helvetica 18')
    label_i.grid(row=i + 2)
    label_i_value.grid(row=i + 2, column=1)

root.mainloop()
