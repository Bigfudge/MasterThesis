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


############### HELPER FUNCTIONS ###############
def remove_tags(word):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', word)
  return cleantext

def db_setup():
	db = sqlite3.connect(constants.main_db)
	cursor = db.cursor()

	#Clears previous table
	cursor.execute('''DROP TABLE IF EXISTS words''')

	#Adds table to db
	cursor.execute('''
 	CREATE TABLE words(id INTEGER PRIMARY KEY, word TEXT, non_alfanum INTEGER,
						tri_grams INTEGER, freq_page INTEGER, vowel INTEGER,
                        word_length INTEGER, get_num_upper INTEGER,
                        has_numbers INTEGER, valid INTEGER)''')
	db.commit()
	db.close()

def create_output_file(db_path, output_filename):
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    cursor.execute('''SELECT word, non_alfanum, tri_grams, freq_page, vowel, word_length, get_num_upper, has_numbers, valid FROM words''')
    data = cursor.fetchall()
    with open(output_filename, 'w') as csvFile:
        writer=csv.writer(csvFile)
        writer.writerows(data)


############### UPDATES METRIC FOR ALL WORDS ###############
def update_metric_non_alfanum(db_path):
    db = sqlite3.connect(db_path)
    cursor= db.cursor()
    cursor.execute('''SELECT word FROM words''')
    rows = cursor.fetchall()
    tot = len(rows)
    count = 1

    for row in rows:
        count +=1
        word = row[0]
        errors = new_non_alfanum(word)
        cursor.execute('''UPDATE words SET non_alfanum = ? WHERE word = ? ''',(errors, word))
        print(str(count)+"/"+str(tot))
    cursor.close()
    db.commit()

def update_metric_word_freq(db_path):
    return null

def update_metric_trigram_freq(db_path, tri_gram_path):
    tri_grams=[]
    db_tri = sqlite3.connect(tri_gram_path)
    db_words = sqlite3.connect(db_path)
    cursor_tri = db_tri.cursor()
    cursor_words = db_words.cursor()

    output=1
    cursor_words.execute('''SELECT word FROM words''')
    for row in cursor_words:
        word = row[0]
        for x in range(len(word)):
            n=word[x:x+3]
            cursor_tri.execute('''SELECT gram, freq FROM tri_grams WHERE gram=?''', (n,))
            user = cursor_tri.fetchone()
            if(user):
                value = user[1]
            else:
                value = 0.1
            output *= value
        cursor_words.execute('''UPDATE words SET tri_grams = ? WHERE word = ? ''',(output, word))
    db_tri.commit()
    db_words.commit()
    db_tri.close()
    db_words.close()

############### CALCULATES METRIC FOR SINGLE WORD ###############
def get_non_alfanum(word):
    errors = list(filter(lambda a: not (a.isalnum() | (a in {'å','ä','ö'})), word))
    return len(errors)
def get_non_alfa(word):
    errors = list(filter(lambda a: not (a.isalpha() | (a in {'å','ä','ö'})), word))
    return len(errors)

def get_word_frequency(word, freq_dict):
    if(word in freq_dict.keys()):
        return freq_dict[word]
    return 0

def get_freq_dict():
    freq_dict = {}
    with open(constants.word_freq_path, 'r') as readFile:
        reader = csv.reader(readFile)
        for line in reader:
            k, v = line
            freq_dict[k]=v
        return freq_dict

def get_trigram_dict():
    freq_dict = {}
    with open(constants.trigrams_path, 'r') as readFile:
        reader = csv.reader(readFile)
        for line in reader:
            k, v = line
            freq_dict[k]=v
        return freq_dict


def get_trigram_freq(word, tri_gram_dict):
    tri_freq=[]
    output=1

    chrs = [c for c in word]
    trigrams= ngrams(chrs,3)

    for gram in trigrams:
        if(gram in tri_gram_dict.keys()):
            output*=(freq[1]/len(freq))
        else:
            output*=0.1

    return output

def word_length(word):
    return(len(word)>13)
def get_num_upper(word):
    return(sum(1 for c in word if c.isupper())>2)
def contains_vowel(word):
    vowels = {"a", "e", "i", "o", "u","å","ä", "ö", "A", "E", "I", "O", "U","Å", "Ä", "Ö"}
    return any(char in vowels for char in word)
def has_numbers(word):
    return any(char.isdigit() for char in word)


############### ADDS WORDS TO DB ###############
def add_ground_truth(input_dir, sample_size):
    count=1
    db = sqlite3.connect(constants.main_db)
    cursor = db.cursor()

    for file in os.listdir(input_dir):
        truth = open(input_dir+file)
        words = [word for line in truth for word in line.split()]
        for word in words:
            if(get_non_alfa(word)==len(word)):
                continue
            if(word[-1] in {'.',',','!','?',':',';','\'','"','-','/'}):
                word= word[:-1]

            freq_dict = get_freq_dict()
            tri_gram_dict= get_trigram_dict()
            cursor.execute('''INSERT INTO words(word, non_alfanum, tri_grams, freq_page, vowel, word_length,get_num_upper,has_numbers, valid)
            VALUES(?,?,?,?,?,?,?,?,?)''', (
            remove_tags(word),
            get_non_alfanum(word),
            get_trigram_freq(word, tri_gram_dict),
            get_word_frequency(word, freq_dict),
            contains_vowel(word),
            word_length(word),
            get_num_upper(word),
            has_numbers(word),
            1))
            count+=1
            if(sample_size):
                if(sample_size<count):
                    break

    db.commit()
    db.close()
    truth.close()

def add_ocr_output(ocr_dir,truth_dir, sample_size):
    count=1
    ocr_dirs=[]
    truth_dirs=[]
    tmp = ocr_dir.split("/")
    filename = "data/"+tmp[-2]+"_"+tmp[-3]+ ".txt"
    db = sqlite3.connect(constants.main_db)
    cursor = db.cursor()

    for file in os.listdir(ocr_dir):
        ocr_dirs.append(ocr_dir+file)
    for file in os.listdir(truth_dir):
            truth_dirs.append(truth_dir+file)

    if(not os.path.isfile(filename)):
        align.main("-sb",ocr_dirs,truth_dirs, filename)

    ocr_errors = open(filename)
    words = [word for line in ocr_errors for word in line.split()]
    for word in words:

        if(get_non_alfa(word)==len(word)):
            continue
        if(word[-1] in {'.',',','!','?',':',';','\'','"','-','/'}):
            word= word[:-1]
        with open(constants.word_freq_path, 'r') as readFile:
            reader = csv.reader(readFile)
            freq = list(reader)
        for item in freq:
            if(item[0]==word):
                continue

        freq_dict = get_freq_dict()
        tri_gram_dict= get_trigram_dict()
        cursor.execute('''INSERT INTO words(word, non_alfanum, tri_grams, freq_page,
        vowel, word_length,get_num_upper,has_numbers, valid)VALUES(?,?,?,?,?,?,?,?,?)''', (
        word,
        get_non_alfanum(word),
        get_trigram_freq(word,tri_gram_dict),
        get_word_frequency(word, freq_dict),
        contains_vowel(word),
        word_length(word),
        get_num_upper(word),
        has_numbers(word),
        0))
        count+=1
        if(sample_size):
            if(sample_size<count):
                break
    db.commit()
    db.close()
    ocr_errors.close()

#Not done#
def add_noisy_words(truth_dir,output_filename):
    for file in os.listdir(truth_dir):
        truth_text = open(truth_dir+file).read()
        words=word_tokenize(truth_text)
        noisy_text=[]
        input_vector=[]
        for word in words:
            noisy_text.append(noise_maker.make_noise(word,0.9))
        output=word_tokenize(' '.join(noisy_text))
        for word in output:
            input_vector.append([remove_tags(word),
                                get_non_alfanum(word),
                                get_trigram_freq(word),
                                get_word_frequency(word),
                                contains_vowel(word)])
        with open(output_filename, 'w') as csvFile:
            writer=csv.writer(csvFile)
            writer.writerows(input_vector)


def gen_trigram_freq(input_files):
    tri_grams = []
    output = {}
    sortedOutput={}
    count=0
    limit=15000

    for file in input_files:
        text= open(file).read()
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
        sortedOutput[key]=value
        count+=1
        if(count>=limit):
            break
    with open(constants.trigrams_path, 'w') as csvFile:
        writer=csv.writer(csvFile)
        writer.writerows(sortedOutput.items())

    return(sortedOutput)



def get_training_data(input_vector, db_path, sample_size):
    if(os.path.isfile(input_vector)):
        os.remove(input_vector)

    if(not os.path.isfile(constants.trigrams_path)):
        gen_trigram_freq([ constants.corpus_dalin,
                            constants.corpus_runeberg,
                            constants.corpus_swedberg])

    if(not os.path.isfile(db_path)):
        db_setup()
        print("Database initilized")
        add_ground_truth('./Evaluation-script/ManuelTranscript/Argus/', sample_size)
        print("Added words (1/6)")
        add_ground_truth('./Evaluation-script/ManuelTranscript/Grepect/', sample_size)
        print("Added words (2/6)")
        add_ocr_output("./Evaluation-script/OCROutput/Ocropus/Argus/","./Evaluation-script/ManuelTranscript/Argus/", sample_size)
        print("Added words (3/6)")
        add_ocr_output("./Evaluation-script/OCROutput/Ocropus/Grepect/","./Evaluation-script/ManuelTranscript/Grepect/", sample_size)
        print("Added words (4/6)")
        add_ocr_output("./Evaluation-script/OCROutput/Tesseract/Argus/","./Evaluation-script/ManuelTranscript/Argus/", sample_size)
        print("Added words (5/6)")
        add_ocr_output("./Evaluation-script/OCROutput/Tesseract/Grepect/","./Evaluation-script/ManuelTranscript/Grepect/", sample_size)
        print("Added words (6/6)")

    create_output_file(db_path,input_vector)

def get_input(file, output_filename):
    ocr_output = open(file, 'r')
    words = [word for line in ocr_output for word in line.split()]
    header=["word","alfanum","trigram","word_freq","vowel","word_length","gen_num_upper","has_number"]
    input_vector=[header]

    for word in words:
        if(get_non_alfa(word)==len(word)):
            continue
        if(word[-1] in {'.',',','!','?',':',';','\'','"','-','/'}):
            word= word[:-1]

        input_vector.append([remove_tags(word),
                            get_non_alfanum(word),
                            get_trigram_freq(word),
                            get_word_frequency(word),
                            contains_vowel(word),
                            word_length(word),
                            get_num_upper(word),
                            has_numbers(word)
                            ])
    ocr_output.close()
    with open(output_filename, 'w') as csvFile:
        writer=csv.writer(csvFile)
        writer.writerows(input_vector)



#get_input("./Evaluation-script/output/OcropusArgus/argus_lb3026335_5_0002.txt","data/input.csv")
# main()
#add_noisy_words(constants.truthArgus,'testArgus.csv')
