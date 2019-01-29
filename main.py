#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import csv
import os
import glob

#Kanske skita i denna???
def prune_word(word):
	if(not word[len(word)-1].isalnum()):
		return(word[:-1])
	return(word)

def contains_non_alfanum(word):
	errors = list(filter(lambda a: not (a.isalnum() | (a in {'-','å','ä','ö'})), word[:-1]))
	return len(errors)
def get_bigram_freq(word):
	return 1
def get_frequency(word):
	return 1
def is_actuall_word(word, truth_file):
	#Returns 1 if 'word' is represented in 'truth_file', otherwise 0
	return 0

def createCSV(input_dir, output_filename):
	for file in os.listdir(input_dir):
		truth = open(input_dir+file)
		words = [word for line in truth for word in line.split()]
		csvData = [[]]
		for word in words:
			#ToDo: Check for duplicates, and only add if unique
			csvData.append([prune_word(word),
							contains_non_alfanum(word),
							get_bigram_freq(word),
							get_frequency(word),
							1])
§
		with open(output_filename, 'a') as csvFile:
		    writer = csv.writer(csvFile)
		    writer.writerows(csvData)

		csvFile.close()
		truth.close()

def main():
	os.remove('input_vector.csv')
	createCSV('./Evaluation-script/ManuelTranscript/Argus/', 'input_vector.csv')
	#createCSV('./Evaluation-script/ManuelTranscript/Grepect/', 'input_vector.csv')


main()
