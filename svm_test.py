import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from numpy import array


#matplotlib inline
label_encoder = LabelEncoder()

df = pd.read_csv("input_vector.csv")
data = df.sample(8000)

values = data[data.columns[0]].values
integer_encoded = label_encoder.fit_transform(values.astype(str))
X=data.drop(data.columns[-1], axis =1)
X=X.drop(data.columns[0],axis=1)
y=data[data.columns[-1]]
X["words"]=integer_encoded

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)
svclassifier = SVC(kernel='rbf')
svclassifier.fit(X_train, y_train)

y_pred = svclassifier.predict(X_test)


print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test,y_pred))
