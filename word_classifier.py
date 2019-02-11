import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from numpy import array
import os
import pickle

def train(path_model, training_data):
    if(not os.path.isfile(path_model)):
        label_encoder = LabelEncoder()

        df = pd.read_csv(training_data)
        data = df.sample(4000)

        values = data[data.columns[0]].values
        integer_encoded = label_encoder.fit_transform(values.astype(str))
        X=data.drop(data.columns[-1], axis =1)
        X=X.drop(data.columns[0],axis=1)
        y=data[data.columns[-1]]
        X["words"]=integer_encoded

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)
        svclassifier = SVC(kernel='linear')
        svclassifier.fit(X_train, y_train)

        pickle.dump(svclassifier, open(path_model, 'wb'))


        return svclassifier
    else:
        svclassifier = pickle.load(open(path_model, 'rb'))
        return svclassifier

        # print(confusion_matrix(y_test,y_pred))
        # print(classification_report(y_test,y_pred))

def predict(input, svclassifier):
    label_encoder = LabelEncoder()

    input_vector=pd.read_csv(input)

    values = input_vector[input_vector.columns[0]].values
    integer_encoded = label_encoder.fit_transform(values.astype(str))
    X=input_vector.drop(input_vector.columns[0],axis=1)
    X["words"]=integer_encoded

    y_pred = svclassifier.predict(X)

    return list(zip(values,y_pred))



def main(input):
    svclassifier = train("models/finalized_model.sav", "data/input_vector.csv")
    predict(input, svclassifier)

main("data/input.csv")
