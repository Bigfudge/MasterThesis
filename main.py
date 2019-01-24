#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

def main():
	ocr = open('ocr_test1.txt')
	truth= open('truth_test1.txt')

	words = [word for line in ocr for word in line.split()]
	
	for word in words:
		test = list(filter(lambda a: not (a.isalnum() | (a in {'å','ä','ö'})), word[:-1]))
		if len(test) > 0:
			print(word)

	ocr.close()
	truth.close()

main()
