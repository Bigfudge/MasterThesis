# Import libraries for data wrangling, preprocessing and visualization
import numpy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
# Importing libraries for building the neural network
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from keras.models import load_model
import os

import keras as K

label_encoder = LabelEncoder()

df = pd.read_csv("input_vector.csv")
data = df.sample(1000)

values = data[data.columns[0]].values
integer_encoded = label_encoder.fit_transform(values.astype(str))
X=data.drop(data.columns[-1], axis =1)
X=X.drop(data.columns[0],axis=1)
y=data[data.columns[-1]]
X["words"]=integer_encoded

def create_baseline():
    # create model
    if(not os.path.isfile("model.h5")):
        my_init = K.initializers.glorot_uniform(seed=1)
        model = Sequential()
        model.add(Dense(8, input_dim=4, kernel_initializer=my_init, activation='tanh'))
        model.add(Dense(8, kernel_initializer=my_init, activation='tanh'))
        model.add(Dense(1, kernel_initializer=my_init, activation='sigmoid'))
        # Compile model. We use the the logarithmic loss function, and the Adam gradient optimizer.
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.save('model.h5')
        return model
    else:
        return load_model('model.h5')
# Evaluate model using standardized dataset.
estimators = []
estimators.append(('standardize', StandardScaler()))
estimators.append(('mlp', KerasClassifier(build_fn=create_baseline, epochs=20, batch_size=5, verbose=0)))

pipeline = Pipeline(estimators)
kfold = StratifiedKFold(n_splits=10, shuffle=True)
results = cross_val_score(pipeline, X, y, cv=kfold)
print("Results: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))

input = pd.read_csv("data/input.csv")
words = input[input.columns[0]].values.astype(str)
integer_encoded = label_encoder.fit_transform(words.astype(str))
input=input.drop(input.columns[0],axis=1)
input["words"]=integer_encoded

pipeline.fit(X,y)
pred=pipeline.predict(input)
print(pred)
