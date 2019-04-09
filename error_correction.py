import xml.etree.ElementTree as ET
import csv
import os
import constants
from Levenshtein import distance
import gen_vector

def extract_words_xml(xml_files):
    all_words={}
    for file in xml_files:
        tree = ET.parse(file)
        root = tree.getroot()
        for text in root:
            for paragraph in text:
                for sentence in paragraph:
                    for word in sentence:
                        if(gen_vector.get_non_alfa(word)==len(word)==1
                            or gen_vector.get_non_alfa(word)==len(word)):
                            continue
                        if(word[-1] in {'.',',','!','?',':',';','\'','"','-','/'}):
                            word= word[:-1]
                        if(str(word.text) not in all_words):
                            all_words[str(word.text)]=0
                        else:
                            all_words[str(word.text)]+=1
    with open(constants.word_freq_path, 'a') as csvFile:
        writer=csv.writer(csvFile)
        writer.writerows(all_words.items())

    return(all_words)

def extract_words_txt(txt_files):
    all_words={}
    for file in txt_files:
        text = open(file)
        words = [word for line in text for word in line.split()]
        for word in words:
            if(gen_vector.get_non_alfa(word)==len(word)==1
                or gen_vector.get_non_alfa(word)==len(word)):
                continue
            if(word[-1] in {'.',',','!','?',':',';','\'','"','-','/'}):
                word= word[:-1]
            if(word not in all_words):
                all_words[word]=0
            else:
                all_words[word]+=1
    with open(constants.word_freq_path, 'a') as csvFile:
        writer=csv.writer(csvFile)
        writer.writerows(all_words.items())
    return(all_words)

def correct_word(word):
    freq=[]
    with open(constants.word_freq_path, 'r') as readFile:
        reader = csv.reader(readFile)
        freq = list(reader)
    edit_dist=1
    candidates=[]
    edit_distances=[]
    for can in freq:
        edit_distances.append([can,distance(can[0],str(word))])
    while (edit_dist < len(str(word))+2 or edit_dist <= 8):
        for item in edit_distances:
            if(item[1]==edit_dist or item[i]==0):
                candidates.append(item[0])
        if(len(candidates)>0):
            #Select candidate with greatest frequency
            winning_candidate=max(candidates, key=lambda x: x[1])
            print("REPLACED %s with %s"%(word,winning_candidate))
            return winning_candidate[0]
        else:
            edit_dist+=1
    #If no candidate is found the original word is returned
    return(word)

def calc_freq(size):
    if(not os.path.isfile(constants.word_freq_path)):
        extract_words_xml([constants.corpus_lag,constants.corpus_tank])
        # extract_words_txt([constants.corpus_dalin])
        # extract_words_txt([constants.corpus_runeberg])
        # extract_words_txt([constants.corpus_swedberg])
        count=0
        for file in os.listdir("./data/corpus/runeberg/"):
            extract_words_txt(["./data/corpus/runeberg/"+file])
            count+=1
            if(size):
                if(count==size):
                    break

def updated_correct_word(word):
    freq=[]
    splits=[]
    candidate=[]

    with open(constants.word_freq_path, 'r') as readFile:
        reader = csv.reader(readFile)
        freq = list(reader)

    for can in freq:
        origin_edit_distances.append([can,distance(can[0],str(word))])
    origin_can, origin_cost = get_candidate(origin_edit_distances, word)
    candidate.append([origin_can, origin_cost])

    #Split words into two
    for i in range(len(word)):
        splits.append(word[:i])
        splits.append(word[i:])

    for var in splits:
        first, second = var
        first_edit_distances=[]
        second_edit_distances=[]

        for can in freq:
            first_edit_distances.append([can,distance(can[0],str(first))])
            second_edit_distances.append([can,distance(can[0],str(second))])

        first_can, first_cost = get_candidate(first_edit_distances, first)
        second_can, second_cost = get_candidate(second_edit_distances, second)

        candidates.append([var, first_cost+second_cost+1])

    winning_candidate=max(candidates, key=lambda x: x[1])
    return winning_candidate


def get_candidate(distance_list, word):
    while (edit_dist < len(str(word))+2 or edit_dist <= 8):
        for item in distance_list:
            if(item[1]==edit_dist):
                candidates.append(item[0])
        if(len(candidates)>0):
            #Select candidate with greatest frequency
            winning_candidate=max(candidates, key=lambda x: x[1])
            print("REPLACED %s with %s"%(word,winning_candidate))
            return winning_candidate[0], edit_dist
        else:
            edit_dist+=1
    else:
        return word, 100
