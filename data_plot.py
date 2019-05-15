import pandas as pd
import numpy as np
import constants as c
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
import math
import gen_vector
import error_correction
import os

def tri_freq_test():
    penta_freq=gen_vector.gen_word_pentagram_freq(1000,'./data/corpus/runeberg/')
    word_freq=error_correction.calc_freq(0, 10000)
    values=[]
    size =0
    while(size <= 20000):
        if(os.path.exists(c.training_data)):
            os.remove(c.training_data)
        if(os.path.exists(c.trigrams_path)):
            os.remove(c.trigrams_path)

        tri_freq=gen_vector.gen_trigram_freq(size)
        gen_vector.get_training_data(c.training_data, c.main_db,13000,tri_freq,penta_freq,word_freq)
        values.append(main())
        print(values)
        size+=500

def word_freq_test():
    penta_freq=gen_vector.gen_word_pentagram_freq(1000,'./data/corpus/runeberg/')
    values=[]
    tri_freq=gen_vector.gen_trigram_freq(1000)
    size =0
    while(size <= 500):
        if(os.path.exists(c.training_data)):
            os.remove(c.training_data)
        if(os.path.exists(c.word_freq_path)):
            os.remove(c.word_freq_path)

        word_freq=error_correction.calc_freq(0, size)
        # print(word_freq.items())
        gen_vector.get_training_data(c.training_data, c.main_db,13000,tri_freq,penta_freq,word_freq)
        values.append(main())
        print(values)
        size+=10
def filter_test():
    values=[]
    penta_freq=gen_vector.gen_word_pentagram_freq(1000,'./data/corpus/runeberg/')
    tri_freq=gen_vector.gen_trigram_freq(1000)
    word_freq=error_correction.calc_freq(0, 1000)
    if(os.path.exists(c.training_data)):
        os.remove(c.training_data)
    gen_vector.get_training_data(c.training_data, c.main_db,13000,tri_freq,penta_freq,word_freq)
    values.append(main())




def main():
    valid=pd.DataFrame()
    errors=pd.DataFrame()

    label_encoder = LabelEncoder()

    df = pd.read_csv(c.training_data)
    data = df

    values = data[data.columns[0]].values
    # print(values)
    integer_encoded = label_encoder.fit_transform(values.astype(str))

    X=data.drop(data.columns[0],axis=1)
    X["words"]=integer_encoded
    valid=X.loc[X[X.columns[-2]] == 1]
    errors=X.loc[X[X.columns[-2]] == 0]
    valid=valid.drop(valid.columns[-2],axis=1)
    errors=errors.drop(errors.columns[-2],axis=1)

    meanValid = [valid[valid.columns[0]].mean(),
            valid[valid.columns[1]].mean(),
            valid[valid.columns[2]].mean(),
            valid[valid.columns[3]].mean(),
            valid[valid.columns[4]].mean(),
            valid[valid.columns[5]].mean(),
            valid[valid.columns[6]].mean()]
    meanError = [errors[errors.columns[0]].mean(),
            errors[errors.columns[1]].mean(),
            errors[errors.columns[2]].mean(),
            errors[errors.columns[3]].mean(),
            errors[errors.columns[4]].mean(),
            errors[errors.columns[5]].mean(),
            errors[errors.columns[6]].mean()]

    test=[]
    for i in range(len(meanError)):
        test.append(perc_diff(meanValid[i],meanError[i]))

    index = ['#Alfanumeric', 'Swedishness', 'Word Frequency','#Vowel', 'Word length','#Uppercase','#Numbers']
    print(test)
    df = pd.DataFrame({'Percent difference metric': test}, index=index)
    ax = df.plot.bar(rot=0, color=['grey'])
    y_pos = range(len(index))
    plt.xticks(y_pos, index, rotation=45, ha="right" )
    plt.subplots_adjust(bottom=0.25)
    plt.show()
    # for i in range(len(index)):
    #     bins = np.linspace(0, 3, 30)
    #     plt.hist(errors[errors.columns[i]], bins, alpha=0.5, normed=True, label='error')
    #     plt.hist(valid[valid.columns[i]], bins, alpha=0.5, normed=True, label='valid')
    #     plt.legend(loc='upper right')
    #     plt.savefig(index[i]+'.png')
    #     plt.close()

    #
    # index = ['#Alfanumeric', 'Swedishness', 'Word Frequency','#Vowel', 'Word length','#Uppercase','#Numbers']
    # # df = pd.DataFrame({'Valid': meanValid,'Error': meanError}, index=index)
    # # ax = df.plot.bar(rot=0, color=['green', 'red'])
    # # y_pos = range(len(index))
    # # plt.xticks(y_pos, index, rotation=45, ha="right" )
    #

def scaled_different_mean(a, b):
    avg= (a+b)/2
    if(avg==0):
        return 0
    return abs(a-b)/avg

def perc_diff(avg_valid, avg_error):
    if(avg_valid>avg_error):
        return 1-(avg_error/avg_valid)
    if(avg_error==0):
        return 0
    return 1-(avg_valid/avg_error)

main()
