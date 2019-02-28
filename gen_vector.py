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
						tri_grams INTEGER, freq_page INTEGER, vowel INTEGER, valid INTEGER)''')
	db.commit()
	db.close()

def create_output_file(db_path, output_filename):
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    cursor.execute('''SELECT word, non_alfanum, tri_grams, freq_page, vowel, valid FROM words''')
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
    errors = list(filter(lambda a: not (a.isalnum() | (a in {'-','å','ä','ö'})), word[:-1]))
    return len(errors)

def get_word_frequency(word, page):
	count=1
	for item in page:
		if(item == word):
			count+=1
	return count/len(page)

def get_trigram_freq(word):
    db_tri = sqlite3.connect(constants.trigrams_db)
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
def get_word_length(word):
    return(len(word))
def get_num_upper(word):
    return(sum(1 for c in word if c.isupper()))
def get_num_lower(word):
        return(sum(1 for c in word if c.islower()))
def contains_vowel(word):
    vowels = {"a", "e", "i", "o", "u","å","ä", "ö", "A", "E", "I", "O", "U","Å", "Ä", "Ö"}
    return any(char in vowels for char in word)



############### ADDS WORDS TO DB ###############
def add_ground_truth(input_dir):

    db = sqlite3.connect(constants.main_db)
    cursor = db.cursor()

    for file in os.listdir(input_dir):
        truth = open(input_dir+file)
        words = [word for line in truth for word in line.split()]
        for word in words:
            if(word[-1] in {'.',',','!','?',':',';','\'','"','-','/'} and len(word)>1):
                words.append(word[-1])
                word= word[:-1]
                cursor.execute('''INSERT INTO words(word, non_alfanum, tri_grams, freq_page, vowel, valid)
                VALUES(?,?,?,?,?,?)''', (remove_tags(word),
                get_non_alfanum(word),
                get_trigram_freq(word),
                get_word_frequency(word,words),
                contains_vowel(word),
                1))

    db.commit()
    db.close()
    truth.close()

def add_ocr_output(ocr_dir,truth_dir):
	ocr_dirs=[]
	truth_dirs=[]
	tmp = ocr_dir.split("/")
	filename = tmp[-2]+"_"+tmp[-3]+ ".txt"
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
		cursor.execute('''INSERT INTO words(word, non_alfanum, tri_grams,
							freq_page, vowel, valid)VALUES(?,?,?,?,?,?)''', (word,
                                                                get_non_alfanum(word),
                                                                get_trigram_freq(word),
                                                                get_word_frequency(word, words),
                                                                contains_vowel(word),
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
	db = sqlite3.connect(constants.trigrams_db)
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



def get_training_data(input_vector, db_path):
    if(os.path.isfile(input_vector)):
        os.remove(input_vector)

    if(not os.path.isfile(db_path)):
        gen_trigram_freq(['./Evaluation-script/ManuelTranscript/Argus/', './Evaluation-script/ManuelTranscript/Grepect/'])

    if(not os.path.isfile(db_path)):
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

    create_output_file(db_path,input_vector)

def get_input(file, output_filename):
    ocr_output = open(file, 'rb')
    words = [word for line in ocr_output for word in line.split()]
    input_vector=[]

    for word in words:
        input_vector.append([remove_tags(str(word)),
                            get_non_alfanum(str(word)),
                            get_trigram_freq(str(word)),
                            get_word_frequency(str(word),words),
                            contains_vowel(str(word))])
    ocr_output.close()
    with open(output_filename, 'w') as csvFile:
        writer=csv.writer(csvFile)
        writer.writerows(input_vector)

def main():
    get_training_data(constants.training_data, constants.main_db)
    # get_input("./Evaluation-script/OCROutput/Ocropus/Argus/ed_pg_a0002_ocropus_twomodel.txt","data/input.csv")
#main()
