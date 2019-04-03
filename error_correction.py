import xml.etree.ElementTree as ET
import csv
import os
import constants
from Levenshtein import distance


def extract_words_xml(xml_files):
    all_words={}
    for file in xml_files:
        tree = ET.parse(file)
        root = tree.getroot()
        for text in root:
            for paragraph in text:
                for sentence in paragraph:
                    for word in sentence:
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
    print(word)
    for can in freq:
        edit_distances.append([can,distance(can[0],str(word))])
    print(len(edit_distances))
    while (edit_dist < len(str(word))+2 or edit_dist <= 8):
        for item in edit_distances:
            if(item[1]==edit_dist):
                candidates.append(item[0])
        if(len(candidates)>0):
            #Select candidate with greatest frequency
            winning_candidate=max(candidates, key=lambda x: x[1])
            #print("REPLACED %s with %s"%(word,winning_candidate))
            return winning_candidate[0]
        else:
            edit_dist+=1
    #If no candidate is found the original word is returned
    print("NO REPLACEMENT")
    return(word)

def calc_freq():
    if(not os.path.isfile(constants.word_freq_path)):
        extract_words_xml([constants.corpus_lag,constants.corpus_tank])
        #extract_words_txt([constants.corpus_dalin])
        #extract_words_txt([constants.corpus_runeberg])
        #extract_words_txt([constants.corpus_swedberg])


def main():
    calc_freq()
main()
