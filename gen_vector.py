#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import csv
import os
import glob
import align
import uuid

#Kanske skita i denna???
def remove_tags(word):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', word)
  return cleantext
def contains_non_alfanum(word):
	errors = list(filter(lambda a: not (a.isalnum() | (a in {'-','å','ä','ö'})), word[:-1]))
	return len(errors)
def get_bigram_freq(word):
	return 1
def get_frequency_in_page(word, page):
	count=1
	for item in page:
		if(item == word):
			count+=1
	return count/len(page)
def is_actuall_word(word, truth_file):
	#Returns 1 if 'word' is represented in 'truth_file', otherwise 0
	return 0

def add_ground_truth(input_dir, output_filename):
	for file in os.listdir(input_dir):
		truth = open(input_dir+file)
		words = [word for line in truth for word in line.split()]
		csvData = [[]]
		for word in words:
			csvData.append([remove_tags(word),
							contains_non_alfanum(word),
							get_bigram_freq(word),
							get_frequency_in_page(word, words),
							1])

		with open(output_filename, 'a') as csvFile:
		    writer = csv.writer(csvFile)
		    writer.writerows(csvData)

		csvFile.close()
		truth.close()

def add_ocr_output(ocr_dir,truth_dir, output_filename):
	ocr_dirs=[]
	truth_dirs=[]
	tmp = ocr_dir.split("/")
	filename = tmp[-2]+"_"+tmp[-3]+ ".txt"
	print(filename)
	for file in os.listdir(ocr_dir):
		ocr_dirs.append(ocr_dir+file)
	for file in os.listdir(truth_dir):
		truth_dirs.append(truth_dir+file)

	if(not os.path.isfile(filename)):
		align.main("-sb",ocr_dirs,truth_dirs, filename)

	ocr_errors = open(filename)
	words = [word for line in ocr_errors for word in line.split()]
	csvData = [[]]
	for word in words:
		csvData.append([word,
						contains_non_alfanum(word),
						get_bigram_freq(word),
						get_frequency_in_page(word, words),
						0])

	with open(output_filename, 'a') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(csvData)

	csvFile.close()
	ocr_errors.close()


def main():
	if(os.path.isfile("input_vector.csv")):
		os.remove('input_vector.csv')
	add_ground_truth('./Evaluation-script/ManuelTranscript/Argus/', 'input_vector.csv')
<<<<<<< HEAD
	# add_ground_truth('./Evaluation-script/ManuelTranscript/Grepect/', 'input_vector.csv')
	add_ocr_output("/Users/simonpersson/Github/MasterThesis/Evaluation-script/OCROutput/Ocropus/Argus/",
					"/Users/simonpersson/Github/MasterThesis/Evaluation-script/ManuelTranscript/Argus/",
					'input_vector.csv')
	# add_ocr_output("/Users/simonpersson/Github/MasterThesis/Evaluation-script/OCROutput/Ocropus/Grepect/",
	# 				"/Users/simonpersson/Github/MasterThesis/Evaluation-script/ManuelTranscript/Grepect/",
	# 				'input_vector.csv')
	# add_ocr_output("/Users/simonpersson/Github/MasterThesis/Evaluation-script/OCROutput/Tesseract/Argus/",
	# 				"/Users/simonpersson/Github/MasterThesis/Evaluation-script/ManuelTranscript/Argus/",
	# 				'input_vector.csv')
	# add_ocr_output("/Users/simonpersson/Github/MasterThesis/Evaluation-script/OCROutput/Tesseract/Grepect/",
	# 				"/Users/simonpersson/Github/MasterThesis/Evaluation-script/ManuelTranscript/Grepect/",
	# 				'input_vector.csv')
=======
	add_ground_truth('./Evaluation-script/ManuelTranscript/Grepect/', 'input_vector.csv')
	add_ocr_output("./Evaluation-script/OCROutput/Ocropus/Argus/",
					"./Evaluation-script/ManuelTranscript/Argus/",
					'input_vector.csv')
	add_ocr_output("./Evaluation-script/OCROutput/Ocropus/Grepect/",
					"./Evaluation-script/ManuelTranscript/Grepect/",
					'input_vector.csv')
	add_ocr_output("./Evaluation-script/OCROutput/Tesseract/Argus/",
					"./Evaluation-script/ManuelTranscript/Argus/",
					'input_vector.csv')
	add_ocr_output("./Evaluation-script/OCROutput/Tesseract/Grepect/",
					"./Evaluation-script/ManuelTranscript/Grepect/",
					'input_vector.csv')
>>>>>>> f4a11ac389f137f7866d98f2888b3cdb9a68fb3d

main()
