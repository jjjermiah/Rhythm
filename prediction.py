from tensorflow import keras
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Activation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
from twilio.rest import Client





test1 = pd.read_csv("test1.csv", header=None)
model = keras.models.load_model("bigboy.h5")
predict = model.predict(test1)



classificationFull = [
    "Normal",
    "Atrial premature, Aberrant atrial premature, Nodal premature, or Supra-ventricular premature",
    " Premature ventricular contraction, or Ventricular escape",
    "Fusion of ventricular and normal",
    "Paced, Fusion of paced and normal, or Unclassifiable",
    
]

classification = ["N", "S", "V", "F", "Q"]

mostLikely = max(predict[0])
for i in range(len(predict[0])):
    if mostLikely == predict[0][i]:
        indexValue = i


print(mostLikely)
print(indexValue)
print("The Patient is likley to have", mostLikely, "of", classificationFull[indexValue])

if indexValue in [0, 3]:
    print("Patient seems to have normal readings")

else:
    account_sid = "AC5cac930f62b3f99fa02d789b619c0573"
    assistant_sid = "UA7a9af8baede328f77501c106277cf181"
    auth_token = "cdd70326b8a39a8bfe3b89a322cdfc32"

    client = Client(account_sid, auth_token)

    call = client.calls.create(
        to="6479723191",
        from_="12262711070",
        url='https://channels.autopilot.twilio.com/v1/AC5cac930f62b3f99fa02d789b619c0573/UA7a9af8baede328f77501c106277cf181/twilio-voice',

    )

    time.sleep(60)

    message = client.messages.create(
             body='Hello caregiver, Your patient Luke Edward seems to be experiencing heart atrial fibrillation, please take necessary actions',
             from_='12262711070',
             to='6479723191'
    )



    print(call.sid)
    print(message.sid)





#print(predict)
#print(model)
