import xml.etree.ElementTree as ET
import csv
import os
import constants
from Levenshtein import distance
import gen_vector
import nltk
from nltk.util import ngrams
import pickle

def save_obj(obj, name ):
    with open('models/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('models/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def extract_words_xml(xml_files):
    all_words={}
    for file in xml_files:
        tree = ET.parse(file)
        root = tree.getroot()
        for text in root:
            for paragraph in text:
                for sentence in paragraph:
                    for word in sentence:
                        if(gen_vector.get_non_alfa(word)==len(word)):
                            continue
                        if(word[-1] in {'.',',','!','?',':',';','\'','"','-','/'}):
                            word= word[:-1]
                        if(str(word.text) not in all_words):
                            all_words[str(word.text)]=0
                        else:
                            all_words[str(word.text)]+=1
    return(all_words)

def extract_words_txt(txt_files):
    all_words={}
    for file in txt_files:
        text = open(file)
        words = [word for line in text for word in line.split()]
        for word in words:
            if(gen_vector.get_non_alfa(word)==len(word)):
                continue
            if(word[-1] in {'.',',','!','?',':',';','\'','"','-','/'}):
                word= word[:-1]
            if(word not in all_words):
                all_words[word]=0
            else:
                all_words[word]+=1
    return(all_words)

def correct_word(word,freq_dict):
    edit_dist=0
    candidates=[]
    edit_distances=[]
    word=str(word)

    for candidate,freq in freq_dict.items():
        edit_distances.append([[candidate,freq],distance(word,candidate)])
    can, cost, freq = get_candidate(edit_distances, word)
    print("REPLACED %s with %s"%(word,can))

    return(can)

def updated_correct_word(word,freq_dict):
    splits=[]
    candidates=[]
    origin_edit_distances=[]
    word=str(word)
    for candidate,freq in freq_dict.items():
        origin_edit_distances.append([[candidate,freq],distance(word,str(candidate))])
    origin_can, origin_cost, origin_freq = get_candidate(origin_edit_distances, word)
    candidates.append([origin_can, origin_cost,origin_freq])

    #Split words into two
    for i in range(1,len(word)):
        splits.append([word[:i],word[i:]])

    for var in splits:
        first, second = var
        first_edit_distances=[]
        second_edit_distances=[]

        for can,freq in freq_dict.items():
            first_edit_distances.append([[can,freq],distance(first,str(can))])
            second_edit_distances.append([[can,freq],distance(second,str(can))])

        first_can, first_cost, first_freq = get_candidate(first_edit_distances, first)
        second_can, second_cost, second_freq = get_candidate(second_edit_distances, second)

        candidates.append([[first_can, second_can], first_cost+second_cost+1, (first_freq+second_freq)/2])

    b = sorted(candidates, key = lambda x: (-x[1], x[2]))
    # print(b)
    winning_candidate=b[-1]
    print("REPLACED %s with %s"%(word,winning_candidate[0]))
    return winning_candidate[0]

def calc_freq(size, limit):
    if(not os.path.isfile(constants.word_freq_path)):
        all_words={}
        sortedOutput={}
        all_words.update(extract_words_xml([constants.corpus_lag,constants.corpus_tank]))
        all_words.update(extract_words_txt([constants.corpus_dalin]))
        all_words.update(extract_words_txt([constants.corpus_runeberg]))
        all_words.update(extract_words_txt([constants.corpus_swedberg]))
        count=0
        for file in os.listdir("./data/corpus/runeberg"):
            all_words.update(extract_words_txt(["./data/corpus/runeberg/"+file]))
            count+=1
            if(size):
                if(count==size):
                    break
        count=0
        for key, value in sorted(all_words.items(), key=lambda item: item[1], reverse=True):
            if(count>=limit):
                break
            sortedOutput[key]=value
            count+=1

        save_obj(sortedOutput, "word_freq")
    else:
        sortedOutput=load_obj("word_freq")

    return(sortedOutput)


def get_candidate(distance_list, word):
    edit_dist=0
    candidates=[]
    while (edit_dist < len(str(word))+2 or edit_dist <= 8):
        for item in distance_list:
            if(item[1]==edit_dist):
                candidates.append(item[0])
        if(len(candidates)>0):
            #Select candidate with greatest frequency
            winning_candidate=max(candidates, key=lambda x: int(x[1]))
            return winning_candidate[0], edit_dist, int(winning_candidate[1])
        else:
            edit_dist+=1
    else:
        return word, 10, 0
