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



############### HELPER FUNCTIONS ###############
def remove_tags(word):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', word)
  return cleantext

def db_setup():
	db = sqlite3.connect('data/data_set.db')
	cursor = db.cursor()

	#Clears previous table
	cursor.execute('''DROP TABLE IF EXISTS words''')

	#Adds table to db
	cursor.execute('''
 	CREATE TABLE words(id INTEGER PRIMARY KEY, word TEXT, non_alfanum INTEGER,
						tri_grams INTEGER, freq_page INTEGER, valid INTEGER)''')
	db.commit()
	db.close()

def create_output_file(db_path, output_filename):
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    cursor.execute('''SELECT word, non_alfanum, tri_grams, freq_page, valid FROM words''')
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
        errors = list(filter(lambda a: not (a.isalnum() | (a in {'-','å','ä','ö'})), word))
        cursor.execute('''UPDATE words SET non_alfanum = ? WHERE word = ? ''',(len(errors), word))
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
    errors = list(filter(lambda a: not (a.isalnum() | (a in {'-','å','ä','ö'})), word[:-1]))
    return len(errors)

def get_word_frequency(word, page):
	count=1
	for item in page:
		if(item == word):
			count+=1
	return count/len(page)

def get_trigram_freq(word):
    db_tri = sqlite3.connect('data/tri_grams.db')
    cursor_tri = db_tri.cursor()
    output=1
    for x in range(len(word)):
        n=word[x:x+3]
        cursor_tri.execute('''SELECT gram, freq FROM tri_grams WHERE gram=?''', (n,))
        user = cursor_tri.fetchone()
        if(user):
            value = user[1]
        else:
            value = 0.1
        output += value

    db_tri.commit()
    db_tri.close()
    return output

############### ADDS WORDS TO DB ###############
def add_ground_truth(input_dir):

	db = sqlite3.connect('data/data_set.db')
	cursor = db.cursor()

	for file in os.listdir(input_dir):
		truth = open(input_dir+file)
		words = [word for line in truth for word in line.split()]
		for word in words:
			cursor.execute('''INSERT INTO words(word, non_alfanum, tri_grams, freq_page, valid)
                  VALUES(?,?,?,?,?)''', (remove_tags(word),
                                        get_non_alfanum(word),
                                        get_trigram_freq(word),
                                        get_word_frequency(word,words),
                                        1))

	db.commit()
	db.close()
	truth.close()

def add_ocr_output(ocr_dir,truth_dir):
	ocr_dirs=[]
	truth_dirs=[]
	tmp = ocr_dir.split("/")
	filename = tmp[-2]+"_"+tmp[-3]+ ".txt"
	db = sqlite3.connect('data/data_set.db')
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
		cursor.execute('''INSERT INTO words(word, non_alfanum, tri_grams,
							freq_page, valid)VALUES(?,?,?,?,?)''', (word,
                                                                get_non_alfanum(word),
                                                                get_trigram_freq(word),
                                                                get_word_frequency(word, words),
                                                                0))
	db.commit()
	db.close()
	ocr_errors.close()

def gen_trigram_freq(input_dirs):

	tri_grams = []
	output = collections.defaultdict(int)
	for input_dir in input_dirs:
		for file in os.listdir(input_dir):
			text= open(input_dir+file).read()
			for x in range(len(text)):
				n=text[x:x+3]
				tri_grams.append(n)
	for gram in tri_grams:
		output[gram] += 1

	#Converts dict to list of tuple
	x = zip(output.keys(), output.values())

	# print(list(x))
	db = sqlite3.connect('data/tri_grams.db')
	cursor = db.cursor()

	#Clears previous table
	cursor.execute('''DROP TABLE IF EXISTS tri_grams''')

	#Adds table to db
	cursor.execute('''
 	CREATE TABLE tri_grams(id INTEGER PRIMARY KEY, gram TEXT, freq INTEGER)
	 			   ''')

	#Adds content
	cursor.executemany(''' INSERT INTO tri_grams(gram, freq) VALUES(?,?)''',list(x))
	db.commit()

	db.close()



def main():
    if(os.path.isfile("input_vector.csv")):
        os.remove('input_vector.csv')

    if(not os.path.isfile("data/tri_grams.db")):
        gen_trigram_freq(['./Evaluation-script/ManuelTranscript/Argus/', './Evaluation-script/ManuelTranscript/Grepect/'])

    if(not os.path.isfile("data/data_set.db")):
        db_setup()
        print("Database initilized")
        add_ground_truth('./Evaluation-script/ManuelTranscript/Argus/')
        print("Added words (1/6)")
        add_ground_truth('./Evaluation-script/ManuelTranscript/Grepect/')
        print("Added words (2/6)")
        add_ocr_output("./Evaluation-script/OCROutput/Ocropus/Argus/","./Evaluation-script/ManuelTranscript/Argus/")
        print("Added words (3/6)")
        add_ocr_output("./Evaluation-script/OCROutput/Ocropus/Grepect/","./Evaluation-script/ManuelTranscript/Grepect/")
        print("Added words (4/6)")
        add_ocr_output("./Evaluation-script/OCROutput/Tesseract/Argus/","./Evaluation-script/ManuelTranscript/Argus/")
        print("Added words (5/6)")
        add_ocr_output("./Evaluation-script/OCROutput/Tesseract/Grepect/","./Evaluation-script/ManuelTranscript/Grepect/")
        print("Added words (6/6)")
    # contains_non_alfanum('data/data_set.db')
    # print("Added metric (1/2)")
    # get_trigram_freq()
    # print("Added metric (2/2)")

    create_output_file('data/data_set.db','input_vector.csv')
main()
