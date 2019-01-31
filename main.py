#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import csv
import os
import glob
import align

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

def add_ground_truth(input_dir, output_filename):
	for file in os.listdir(input_dir):
		truth = open(input_dir+file)
		words = [word for line in truth for word in line.split()]
		csvData = [[]]
		for word in words:
			csvData.append([prune_word(word),
							contains_non_alfanum(word),
							get_bigram_freq(word),
							get_frequency(word),
							1])

		with open(output_filename, 'a') as csvFile:
		    writer = csv.writer(csvFile)
		    writer.writerows(csvData)

		csvFile.close()
		truth.close()

def test():
	errors = open("demofile.txt")
	words = [word for line in errors for word in line.split()]
	for word in words:
		if "°°" in word:
			print(word.replace('°','')+ "\n")
def add_ocr_output(ocr_dir,truth_dir, output_filename):
	ocr_dirs=[]
	truth_dirs=[]
	filename = "ocr_errors.txt"

	for file in os.listdir(ocr_dir):
		ocr_dirs.append(ocr_dir+file)
	for file in os.listdir(truth_dir):
		truth_dirs.append(truth_dir+file)

	#align.main("-sb",ocr_dirs,truth_dirs, filename)

	ocr_errors = open(filename)
	words = [word for line in ocr_errors for word in line.split()]
	csvData = [[]]
	for word in words:
		csvData.append([word,
						contains_non_alfanum(word),
						get_bigram_freq(word),
						get_frequency(word),
						0])

	with open(output_filename, 'a') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(csvData)

	csvFile.close()
	ocr_errors.close()


def main():
	#os.remove('input_vector.csv')
	add_ground_truth('./Evaluation-script/ManuelTranscript/Argus/', 'input_vector.csv')
	#createCSV('./Evaluation-script/ManuelTranscript/Grepect/', 'input_vector.csv')
	add_ocr_output("/Users/simonpersson/Github/MasterThesis/Evaluation-script/OCROutput/Ocropus/Argus/",
					"/Users/simonpersson/Github/MasterThesis/Evaluation-script/ManuelTranscript/Argus/",
					'input_vector.csv')

main()
