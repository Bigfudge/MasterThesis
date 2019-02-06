import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
#matplotlib inline

df = pd.read_csv("input_vector.csv")
data = df.sample(50000)

X=data.drop(df.columns[-1], axis =1)
X=X.drop(df.columns[0],axis=1)
y=data[df.columns[-1]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)

svclassifier = SVC(kernel='linear')
svclassifier.fit(X_train, y_train)

y_pred = svclassifier.predict(X_test)

print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test,y_pred))
