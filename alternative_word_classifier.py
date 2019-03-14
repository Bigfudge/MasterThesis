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
import constants as c

import keras as K
def is_non_zero_file(fpath):
    return True if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else False


def get_data(training_data):
    label_encoder = LabelEncoder()

    df = pd.read_csv(training_data)
    data = df.sample(8000)

    values = data[data.columns[0]].values
    integer_encoded = label_encoder.fit_transform(values.astype(str))
    X=data.drop(data.columns[-1], axis =1)
    X=X.drop(data.columns[0],axis=1)

    y=data[data.columns[-1]]
    X["words"]=integer_encoded
    return X,y

def build_model():

    if(not os.path.isfile("models/model.h5")):
        X, y = get_data(c.training_data)

        my_init = K.initializers.glorot_uniform(seed=1)
        model = Sequential()
        model.add(Dense(64, input_dim=5, kernel_initializer=my_init, activation='tanh'))
        model.add(Dense(32, kernel_initializer=my_init, activation='tanh'))
        model.add(Dense(32, kernel_initializer=my_init, activation='tanh'))
        model.add(Dense(16, kernel_initializer=my_init, activation='tanh'))

        model.add(Dense(1, kernel_initializer=my_init, activation='sigmoid'))
        # Compile model. We use the the logarithmic loss function, and the Adam gradient optimizer.
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        # model.save('models/model.h5')
        return model

    else:
        return load_model('models/model.h5')

def train(model_path, training_data):
    if(not os.path.isfile(model_path)):
        X, y = get_data(training_data)
        # Evaluate model using standardized dataset.
        estimators = []
        estimators.append(('standardize', StandardScaler()))
        estimators.append(('mlp', KerasClassifier(build_fn=build_model, epochs=20, batch_size=5, verbose=1)))
        pipeline = Pipeline(estimators)

        kfold = StratifiedKFold(n_splits=10, shuffle=True)
        results = cross_val_score(pipeline, X, y, cv=kfold)
        pipeline.fit(X, y)
        pickle.dump(svclassifier, open(path_model, 'wb'))

        print("Results: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
        return(pipeline)
    else:
        pipeline = pickle.load(open(path_model, 'rb'))
        return pipeline

def predict(input, model):
    label_encoder = LabelEncoder()
    y_pred=[]
    if( not is_non_zero_file(input)):
        return y_pred
    input_vector=pd.read_csv(input)

    values = input_vector[input_vector.columns[0]].values
    integer_encoded = label_encoder.fit_transform(values.astype(str))
    X=input_vector.drop(input_vector.columns[0],axis=1)
    X["words"]=integer_encoded

    pred=model.predict(X)
    print(pred)

model = train(c.training_data)
predict(c.input, model)
# input = pd.read_csv("data/input.csv")
# words = input[input.columns[0]].values.astype(str)
# integer_encoded = label_encoder.fit_transform(words.astype(str))
# input=input.drop(input.columns[0],axis=1)
# input["words"]=integer_encoded
#
# pipeline.fit(X,y)
# pred=pipeline.predict(input)
# print(pred)
