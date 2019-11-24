# import crypto libraries
from cn.protect import Protect
from cn.protect.privacy import KAnonymity
from cn.protect.hierarchy import DataHierarchy, OrderHierarchy, IntervalHierarchy
from cn.protect.quality import Loss
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Activation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


mitTestData = pd.read_csv("mitbih_test.csv", header=None)
mitTrainData = pd.read_csv("mitbih_train.csv", header=None)
# drop missing values
mitTrainData = pd.concat([mitTrainData, mitTestData], axis=0)

# privacy model
prot=Protect(mitTrainData, KAnonymity(5))
# quality model
prot.quality_model = Loss()
# no more than 10% of rows will be redacted
prot.suppression = .1
# create hierarchies automatically
prot.hierarchies.age = OrderHierarchy('interval', 5, 2, 2)
# return an anonymized dataframe
priv = prot.protect()

mitTrainData = priv

print("MIT test dataset")
print(mitTestData.info())
print("MIT train dataset")
print(mitTrainData.info())

# take a random distribution
sample = mitTestData.sample(5)

# remove the target column
sampleX = sample.iloc[:,sample.columns != 187]

#Use mat lab to create the graph
plt.style.use('classic')

# plt samples, iterate through the rows and plot it on the graph
for index, row in sampleX.iterrows():
    plt.plot(np.array(range(0, 187)) ,row)

#Create title and graph labels
plt.xlabel("time")
plt.ylabel("magnitude")
plt.title("heartbeat reccording \nrandom sample")

#Draw line graph
plt.show()

#Create bar graph
plt.style.use("ggplot")

#Draw title
plt.title("Number of record in each category")

#Input bar graph data
plt.hist(sample.iloc[:,sample.columns == 187].transpose())

#Draw bar graph
plt.show()

#Start training and testing data
print("Train data")
print("Type\tCount")

#Note that 187 is the max number of columns
#Printing the number of unique values in the data set
print((mitTrainData[187]).value_counts())
print("-------------------------")
print("Test data")
print("Type\tCount")
print((mitTestData[187]).value_counts())

#X axis data
print("--- X ---")
X = mitTrainData.loc[:, mitTrainData.columns != 187]
print(X.head())
print(X.info())

#Y axis data
print("--- Y ---")
y = mitTrainData.loc[:, mitTrainData.columns == 187]
y = to_categorical(y)

#X axis testing
print("--- testX ---")
testX = mitTestData.loc[:, mitTestData.columns != 187]
print(testX.head())
print(testX.info())

#Y axis testing
print("--- testy ---")
testy = mitTestData.loc[:, mitTestData.columns == 187]
testy = to_categorical(testy)

#Create Convulational Neural Network Model (Deep Learning)
model = Sequential()

model.add(Dense(50, activation='relu', input_shape=(187,)))
model.add(Dense(50, activation='relu'))
model.add(Dense(5, activation='softmax'))

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(X, y, epochs = 100)
model.save("rhythmModel.h5")

print("Evaluation: ")
mse, acc = model.evaluate(testX, testy)
print('mean_squared_error :', mse)
print('accuracy:', acc)
