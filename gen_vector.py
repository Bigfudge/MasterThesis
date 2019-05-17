#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import csv
import os
import glob
import align
import uuid
import collections
import sqlite3
import constants
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import noise_maker
import nltk
from nltk.util import ngrams
import math
import pickle
import accuracyScript


############### HELPER FUNCTIONS ###############
def remove_tags(word):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', word)
  return cleantext

def save_obj(obj, name ):
    with open('models/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('models/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

############### CALCULATES METRIC FOR SINGLE WORD ###############
def get_non_alfanum(word):
    errors = list(filter(lambda a: not (a.isalnum() | (a in {'å','ä','ö'})), word))
    return len(errors)

def get_non_alfa(word):
    errors = list(filter(lambda a: not (a.isalpha() | (a in {'å','ä','ö'})), word))
    return len(errors)

def get_word_frequency(word, freq_dict):
    if(word in freq_dict):
        return int(freq_dict[word])/len(freq_dict)
    return 0

def get_trigram_freq(word, tri_gram_dict):
    output=1
    chrs = [c for c in word]
    trigrams= ngrams(chrs,3)
    for gram in trigrams:
        if(gram in tri_gram_dict):
            output*=tri_gram_dict[gram]/len(tri_gram_dict)
        else:
            output*=0.001
    return output

def get_pentagram_freq(context, penta_gram_dict):
    if(tuple(context) in penta_gram_dict):
        print(freq[1]/len(freq))
        print("PENTA")
        return freq[1]/len(freq)
    else:
        return 0

def word_length(word):
    return(len(word)>13)

def get_num_upper(word):
    count=0
    for char in word:
        if(char.isupper()):
            count+=1
    return count

def contains_vowel(word):
    vowels = {"a", "e", "i", "o", "u","å","ä", "ö", "A", "E", "I", "O", "U","Å", "Ä", "Ö"}
    return any(char in vowels for char in word)

def has_numbers(word):
    count=0
    for char in word:
        if(char.isdigit()):
            count+=1
    return count

def get_context(count, words):
    if(count==0):
        return tuple(words[count:count+6])
    elif(count==1):
        return tuple(words[count-1:count+5])
    elif(count==len(words)-2):
        return tuple(words[count-3:count+2])
    elif(count==len(words)-1):
        return tuple(words[count-4:count+1])
    else:
        return tuple(words[count-3:count+3])

############### ADDS WORDS TO DB ###############
def add_ground_truth(input_dir, sample_size,tri_gram_dict,penta_freq,word_freq):
    count=1
    output=[]

    for file in os.listdir(input_dir):
        truth = open(input_dir+file)
        words = [word for line in truth for word in line.split()]
        i=0
        for word in words:
            if(get_non_alfa(word)==len(word)):
                continue
            if(word[-1] in {'.',',','!','?',':',';','\'','"','-','/'}):
                word= word[:-1]

            output.append([
                        remove_tags(word),
                        get_non_alfanum(word),
                        get_trigram_freq(word, tri_gram_dict),
                        get_word_frequency(word, word_freq),
                        contains_vowel(word),
                        word_length(word),
                        get_num_upper(word),
                        has_numbers(word),
                        1])
            i+=1
            if(sample_size):
                if(sample_size<count):
                    return output
            count+=1

    return output

def add_ocr_output(ocr_dir,truth_dir, sample_size,tri_gram_dict,penta_freq,word_freq, error_words, source):
    count=1
    ocr_dirs=[]
    truth_dirs=[]
    output=[]

    if(not os.path.isfile("models/"+error_words+".pkl")):
        pairs=accuracyScript.get_pair(ocr_dir, truth_dir, source)
        for pair in pairs:
            if(len(pair)!=2):
                continue
            ocr_file, truth_file = pair
            ocr_dirs.append(ocr_dir+ocr_file)
            truth_dirs.append(truth_dir+truth_file)
        words=align.main("-sb",ocr_dirs,truth_dirs, error_words)
    else:
        words=load_obj(error_words)

    i=0
    for word in words:

        if len(word)==0:
            continue
        if(get_non_alfa(word)==len(word)):
            continue
        if(word[-1] in {'.',',','!','?',':',';','\'','"','-','/'}):
            word= word[:-1]

        output.append([
                    word,
                    get_non_alfanum(word),
                    get_trigram_freq(word,tri_gram_dict),
                    get_word_frequency(word, word_freq),
                    contains_vowel(word),
                    word_length(word),
                    get_num_upper(word),
                    has_numbers(word),
                    0])
        if(sample_size):
            if(sample_size<count):
                return output
        count+=1
    return output

def gen_trigram_freq(limit):
    if(not os.path.isfile(constants.trigrams_path)):
        tri_grams = []
        output = {}
        sortedOutput={}
        count=0
        input_files= [  constants.corpus_dalin,
                        constants.corpus_runeberg,
                        constants.corpus_swedberg]
        for file in os.listdir("./data/corpus/runeberg"):
            input_files.append("./data/corpus/runeberg/"+file)

        for file in input_files:
            text= open(file).read()
            # text =text.replace('\n','')
            chrs = [c for c in text]
            trigrams= ngrams(chrs,3)
            for gram in trigrams:
                tri_grams.append(tuple(gram))

        for gram in tri_grams:
            if(gram not in output):
                output[gram]=1
            else:
                output[gram]+=1

        for key, value in sorted(output.items(), key=lambda item: item[1], reverse=True):
            if(count>=limit):
                break
            sortedOutput[key]=value
            count+=1

        save_obj(sortedOutput, "tri_gram")
    else:
        sortedOutput=load_obj("tri_gram")

    return(sortedOutput)

def gen_word_pentagram_freq(size, input_dir):
    if(not os.path.isfile(constants.pentagrams_path)):
        penta_grams = []
        output = {}
        sortedOutput={}
        count=0
        all_words=[]
        for file in os.listdir(input_dir):
            truth = open(input_dir+file)
            words = [word for line in truth for word in line.split()]
            for word in words:
                if(get_non_alfa(word)==len(word)):
                    continue
                if(word[-1] in {'.',',','!','?',':',';','\'','"','-','/'}):
                    word= word[:-1]
                all_words.append(word)
        pentagrams = ngrams(all_words, 5)
        for gram in pentagrams:
            penta_grams.append(tuple(gram))

        for gram in penta_grams:
            if(gram not in output):
                output[gram]=1
            else:
                output[gram]+=1
        count=0
        for key, value in sorted(output.items(), key=lambda item: item[1], reverse=True):
            sortedOutput[key]=value
            count+=1
            if(count>=size):
                break
        save_obj(sortedOutput, "penta_gram")
    else:
        sortedOutput=load_obj("penta_gram")

    return(sortedOutput)



def get_training_data(input_vector, db_path, sample_size,tri_freq,penta_freq,word_freq):
    training_data=[]

    if(not os.path.isfile(input_vector)):
        training_data.extend(add_ground_truth('./Evaluation-script/ManuelTranscript/Argus/', sample_size,tri_freq,penta_freq,word_freq))
        print("Added words (1/8)")
        training_data.extend(add_ground_truth('./Evaluation-script/ManuelTranscript/Grepect/', sample_size,tri_freq,penta_freq,word_freq))
        print("Added words (2/8)")
        training_data.extend(add_ground_truth('./Evaluation-script/ManuelTranscript/Argus/', sample_size,tri_freq,penta_freq,word_freq))
        print("Added words (3/8)")
        training_data.extend(add_ground_truth('./Evaluation-script/ManuelTranscript/Grepect/', sample_size,tri_freq,penta_freq,word_freq))
        print("Added words (4/8)")
        training_data.extend(add_ocr_output("./Evaluation-script/OCROutput/Ocropus/Argus/","./Evaluation-script/ManuelTranscript/Argus/", sample_size,tri_freq,penta_freq,word_freq, constants.error_words_OcropusArgus, 'Argus'))
        print("Added words (5/8)")
        training_data.extend(add_ocr_output("./Evaluation-script/OCROutput/Ocropus/Grepect/","./Evaluation-script/ManuelTranscript/Grepect/", sample_size,tri_freq,penta_freq,word_freq, constants.error_words_OcropusGrepect, 'Grepect'))
        print("Added words (6/8)")
        training_data.extend(add_ocr_output("./Evaluation-script/OCROutput/Tesseract/Argus/","./Evaluation-script/ManuelTranscript/Argus/", sample_size,tri_freq,penta_freq,word_freq, constants.error_words_TesseractArgus, 'Argus'))
        print("Added words (7/8)")
        training_data.extend(add_ocr_output("./Evaluation-script/OCROutput/Tesseract/Grepect/","./Evaluation-script/ManuelTranscript/Grepect/", sample_size,tri_freq,penta_freq,word_freq, constants.error_words_TesseractGrepect, 'Grepect'))
        print("Added words (8/8)")
        with open(input_vector, 'w') as csvFile:
            writer=csv.writer(csvFile)
            writer.writerows(training_data)

def get_input(file, output_filename,tri_freq_dict,penta_freq,word_freq):
    ocr_output = open(file, 'r')
    words = [word for line in ocr_output for word in line.split()]
    header=["word","alfanum","trigram","word_freq","vowel","word_length","gen_num_upper","has_number"]
    input_vector=[header]

    i=0
    for word in words:
        if(get_non_alfa(word)==len(word)):
            continue
        # if(word[-1] in {'.',',','!','?',':',';','\'','"','-','/'}):
        #     word= word[:-1]
        input_vector.append([remove_tags(word),
                            get_non_alfanum(word),
                            get_trigram_freq(word, tri_freq_dict),
                            get_word_frequency(word, word_freq),
                            contains_vowel(word),
                            word_length(word),
                            get_num_upper(word),
                            has_numbers(word)
                            ])
        i+=1
    ocr_output.close()

    with open(output_filename, 'w') as csvFile:
        writer=csv.writer(csvFile)
        writer.writerows(input_vector)
