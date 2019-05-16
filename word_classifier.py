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
import constants
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler

# from sklearn import svm
import numpy


def is_non_zero_file(fpath):
    return True if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else False


def svc_param_selection(X, y, nfolds):
    Cs=     [0.0001, 0.01, 1, 100, 1000, 10000]
    gammas =[0.0001, 0.01, 1, 100, 1000, 10000]
    param_grid = {'C': Cs, 'gamma' : gammas}
    grid_search = GridSearchCV(SVC(kernel='rbf'), param_grid, cv=nfolds)
    grid_search.fit(X, y)
    grid_search.best_params_
    return grid_search.best_params_

def train(path_model, training_data, sample_size, svm_kernal, c_value,gamma):
    if(not os.path.isfile(path_model)):
        label_encoder = LabelEncoder()

        df = pd.read_csv(training_data)
        data = df.sample(sample_size)

        values = data[data.columns[0]].values
        integer_encoded = label_encoder.fit_transform(values.astype(str))
        X=data.drop(data.columns[-1], axis =1)
        X=X.drop(data.columns[0],axis=1)

        y=data[data.columns[-1]]

        # X["words"]=integer_encoded
        # print(svc_param_selection(X, y, 5))
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)

        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
        svclassifier = SVC(kernel=svm_kernal, C=c_value, gamma=gamma, verbose=1)
        svclassifier.fit(X_train, y_train)

        y_pred = svclassifier.predict(X_test)

        pickle.dump(svclassifier, open(path_model, 'wb'))
        print(confusion_matrix(y_test,y_pred))
        print(classification_report(y_test,y_pred))

    else:
        svclassifier = pickle.load(open(path_model, 'rb'))

    return svclassifier



def predict(input, svclassifier):
    label_encoder = LabelEncoder()
    y_pred=[]
    if( not is_non_zero_file(input)):
        return y_pred
    input_vector=pd.read_csv(input)
    if(len(input_vector)==0):
        return []
    values = input_vector[input_vector.columns[0]].values
    # print(values)
    integer_encoded = label_encoder.fit_transform(values.astype(str))
    X=input_vector.drop(input_vector.columns[0],axis=1)
    # X["words"]=integer_encoded
    sc = StandardScaler()
    X = sc.fit_transform(X)


    y_pred = svclassifier.predict(X)

    print(list(zip(values,y_pred)))
    return list(zip(values,y_pred))

def get_performace_report(path_model, training_data, sample_size, svm_kernal, c_value,gamma):
    label_encoder = LabelEncoder()

    df = pd.read_csv(training_data)
    data = df.sample(sample_size)

    values = data[data.columns[0]].values
    integer_encoded = label_encoder.fit_transform(values.astype(str))
    X=data.drop(data.columns[-1], axis =1)
    X=X.drop(data.columns[0],axis=1)

    y=data[data.columns[-1]]
    # X["words"]=integer_encoded
    # params=svc_param_selection(X,y,3)
    # print(params)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)
    svclassifier = SVC(kernel=svm_kernal, C=c_value, gamma=gamma)
    svclassifier.fit(X_train, y_train)

    y_pred = svclassifier.predict(X_test)
    print(confusion_matrix(y_test,y_pred))
    print(classification_report(y_test,y_pred))
    return classification_report(y_test,y_pred)


def main(input):
    svclassifier = train(constants.svm_model, constants.training_data)
    predict(input, svclassifier)

# train('test.sav', constants.training_data, 10000)# main("data/input.csv")
