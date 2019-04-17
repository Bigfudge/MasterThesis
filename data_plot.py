import pandas as pd
import numpy
import constants as c
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler



def main():
    valid=pd.DataFrame()
    errors=pd.DataFrame()

    label_encoder = LabelEncoder()

    df = pd.read_csv(c.training_data)
    data = df
    values = data[data.columns[0]].values
    integer_encoded = label_encoder.fit_transform(values.astype(str))
    X=data.drop(data.columns[0],axis=1)
    # sc = StandardScaler()
    #X = sc.fit_transform(X)

    valid=X.loc[X[X.columns[-1]] == 1]
    errors=X.loc[X[X.columns[-1]] == 0]
    # X["words"]=integer_encoded

    test=errors.loc[errors[errors.columns[1]] > 0]
    print(test)

    meanValid = [valid[valid.columns[0]].mean(),
            valid[valid.columns[1]].mean(),
            valid[valid.columns[2]].mean(),
            valid[valid.columns[3]].mean(),
            valid[valid.columns[4]].mean(),
            valid[valid.columns[5]].mean(),
            valid[valid.columns[6]].mean(),
            valid[valid.columns[7]].mean()]
    meanError = [errors[errors.columns[0]].mean(),
            errors[errors.columns[1]].mean(),
            errors[errors.columns[2]].mean(),
            errors[errors.columns[3]].mean(),
            errors[errors.columns[4]].mean(),
            errors[errors.columns[5]].mean(),
            errors[errors.columns[6]].mean(),
            errors[errors.columns[7]].mean()]

    print(valid[valid.columns[2]].mean())
    print(errors[errors.columns[2]].mean())

    index = ['alfanum', 'swedishness', 'word_freq_page','Vowel', 'word_length','get_num_upper','has_numbers','next']
    df = pd.DataFrame({'Valid': meanValid,'Error': meanError}, index=index)
    ax = df.plot.bar(rot=0, color=['green', 'red'])
    plt.show()

main()
