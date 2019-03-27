import pandas as pd
import numpy
import constants as c
import matplotlib.pyplot as plt



def main():
    valid=pd.DataFrame()
    errors=pd.DataFrame()


    df = pd.read_csv(c.training_data)
    data = df.sample(100000)

    X=data.drop(data.columns[0],axis=1)

    valid=X.loc[X[X.columns[-1]] == 1]
    errors=X.loc[X[X.columns[-1]] == 0]





    meanValid = [valid[valid.columns[0]].mean(),
            valid[valid.columns[1]].mean()/800,
            valid[valid.columns[2]].mean(),
            valid[valid.columns[3]].mean()]
    meanError = [errors[errors.columns[0]].mean(),
            errors[errors.columns[1]].mean()/800,
            errors[errors.columns[2]].mean(),
            errors[errors.columns[3]].mean()]


    index = ['alfanum', 'swedishness', 'word_freq_page','Vowel']
    df = pd.DataFrame({'Error': meanValid,'Valid': meanError}, index=index)
    ax = df.plot.bar(rot=0, color=['red', 'green'])
    plt.show()

main()