#!/bin/sh
from subprocess import call
import os
import shutil
import glob
import subprocess
import constants as c

def	run_acc(genPath, truthPath, reportPath, frontierPath, command, engine):
	pairOfPaths= []
	for gen in os.listdir(genPath):
		pairOfPaths.append([gen])
	if(engine=="Ocropus"):
		for truth in os.listdir(truthPath):
			for	match in pairOfPaths:
				gen = match[0]
				if(gen[:10]==truth[:10]):
					match.append(truth)
	elif(engine=="Tesseract"):
		for truth in os.listdir(truthPath):
			for	match in pairOfPaths:
				gen = match[0]
				if(gen[-4:]==truth[-4:]):
					match.append(truth)
	else:
		print("Wrong engine")
	count=0
	if len(os.listdir(reportPath) ) != 0:
		os.system('rm ' + reportPath+"*")
	for	item in pairOfPaths:
		call([frontierPath+command,truthPath+item[1],genPath+item[0],
				reportPath+"accuracy_report_"+str(count)])
		count += 1

def	combinedAcc(reportPath, frontierPath, command, outputFile):
	all_reports = [report for report in glob.glob(reportPath + '/*')]
	command = [frontierPath+command] + all_reports
	p = subprocess.Popen(command,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = p.communicate()
	if error:
		print("ERROR", e)
	with open(outputFile, 'w') as fd:
		fd.write(output)

def completeEvaluation():
	run_acc(c.genOcropusArgus, c.truthArgus, c.charReportOcropusArgus, c.frontierPath, "accuracy", "Ocropus")
	run_acc(c.genOcropusGrepect, c.truthGrepect, c.charReportOcropusGrepact, c.frontierPath, "accuracy", "Ocropus")
	run_acc(c.genTesseractArgus, c.truthArgus, c.charReportTesseractArgus, c.frontierPath, "accuracy", "Tesseract")
	run_acc(c.genTesseractGrepect, c.truthGrepect, c.charReportTesseractGrepect, c.frontierPath, "accuracy","Tesseract")

	run_acc(c.outputOcropusArgus, c.truthArgus, c.outputCharReportOcropusArgus, c.frontierPath, "accuracy", "Ocropus")
	run_acc(c.outputOcropusGrepect, c.truthGrepect, c.outputCharReportOcropusGrepact, c.frontierPath, "accuracy", "Ocropus")
	run_acc(c.outputTesseractArgus, c.truthArgus, c.outputCharReportTesseractArgus, c.frontierPath, "accuracy", "Tesseract")
	run_acc(c.outputTesseractGrepect, c.truthGrepect, c.outputCharReportTesseractGrepect, c.frontierPath, "accuracy","Tesseract")


	combinedAcc(c.charReportOcropusArgus, c.frontierPath, "accsum", "CharAcc_OcropusArgus.txt")
	combinedAcc(c.charReportOcropusGrepact, c.frontierPath, "accsum", "CharAcc_OcropusGrepect.txt")
	combinedAcc(c.charReportTesseractArgus, c.frontierPath, "accsum", "CharAcc_TesseractArgus.txt")
	combinedAcc(c.charReportTesseractGrepect, c.frontierPath, "accsum", "CharAcc_TesseractGrepect.txt")

	combinedAcc(c.outputCharReportOcropusArgus, c.frontierPath, "accsum", "Output_CharAcc_OcropusArgus.txt")
	combinedAcc(c.outputCharReportOcropusGrepact, c.frontierPath, "accsum", "Output_CharAcc_OcropusGrepect.txt")
	combinedAcc(c.outputCharReportTesseractArgus, c.frontierPath, "accsum", "Output_CharAcc_TesseractArgus.txt")
	combinedAcc(c.outputCharReportTesseractGrepect, c.frontierPath, "accsum", "Output_CharAcc_TesseractGrepect.txt")


	run_acc(c.genOcropusArgus, c.truthArgus, c.wordReportOcropusArgus, c.frontierPath, "wordacc", "Ocropus")
	run_acc(c.genOcropusGrepect, c.truthGrepect, c.wordReportOcropusGrepact, c.frontierPath, "wordacc", "Ocropus")
	run_acc(c.genTesseractArgus, c.truthArgus, c.wordReportTesseractArgus, c.frontierPath, "wordacc", "Tesseract")
	run_acc(c.genTesseractGrepect, c.truthGrepect, c.wordReportTesseractGrepect, c.frontierPath, "wordacc","Tesseract")

	run_acc(c.outputOcropusArgus, c.truthArgus, c.outputWordReportOcropusArgus, c.frontierPath, "wordacc", "Ocropus")
	run_acc(c.outputOcropusGrepect, c.truthGrepect, c.outputWordReportOcropusGrepact, c.frontierPath, "wordacc", "Ocropus")
	run_acc(c.outputTesseractArgus, c.truthArgus, c.outputWordReportTesseractArgus, c.frontierPath, "wordacc", "Tesseract")
	run_acc(c.outputTesseractGrepect, c.truthGrepect, c.outputWordReportTesseractGrepect, c.frontierPath, "wordacc","Tesseract")

	combinedAcc(c.wordReportOcropusArgus, c.frontierPath, "wordaccsum", "WordAcc_OcropusArgus.txt")
	combinedAcc(c.wordReportOcropusGrepact, c.frontierPath, "wordaccsum", "WordAcc_OcropusGrepect.txt")
	combinedAcc(c.wordReportTesseractArgus, c.frontierPath, "wordaccsum", "WordAcc_TesseractArgus.txt")
	combinedAcc(c.wordReportTesseractGrepect, c.frontierPath, "wordaccsum", "WordAcc_TesseractGrepect.txt")

	combinedAcc(c.outputWordReportOcropusArgus, c.frontierPath, "wordaccsum", "WordAcc_OcropusArgus.txt")
	combinedAcc(c.outputWordReportOcropusGrepact, c.frontierPath, "wordaccsum", "WordAcc_OcropusGrepect.txt")
	combinedAcc(c.outputWordReportTesseractArgus, c.frontierPath, "wordaccsum", "WordAcc_TesseractArgus.txt")
	combinedAcc(c.outputWordReportTesseractGrepect, c.frontierPath, "wordaccsum", "WordAcc_TesseractGrepect.txt")

def outputEvaluation():
	run_acc(c.outputOcropusArgus, c.truthArgus, c.outputCharReportOcropusArgus, c.frontierPath, "accuracy", "Ocropus")
	run_acc(c.outputOcropusGrepect, c.truthGrepect, c.outputCharReportOcropusGrepact, c.frontierPath, "accuracy", "Ocropus")
	run_acc(c.outputTesseractArgus, c.truthArgus, c.outputCharReportTesseractArgus, c.frontierPath, "accuracy", "Tesseract")
	run_acc(c.outputTesseractGrepect, c.truthGrepect, c.outputCharReportTesseractGrepect, c.frontierPath, "accuracy","Tesseract")

	combinedAcc(c.outputCharReportOcropusArgus, c.frontierPath, "accsum", "Output_CharAcc_OcropusArgus.txt")
	combinedAcc(c.outputCharReportOcropusGrepact, c.frontierPath, "accsum", "Output_CharAcc_OcropusGrepect.txt")
	combinedAcc(c.outputCharReportTesseractArgus, c.frontierPath, "accsum", "Output_CharAcc_TesseractArgus.txt")
	combinedAcc(c.outputCharReportTesseractGrepect, c.frontierPath, "accsum", "Output_CharAcc_TesseractGrepect.txt")

	run_acc(c.outputOcropusArgus, c.truthArgus, c.outputWordReportOcropusArgus, c.frontierPath, "wordacc", "Ocropus")
	run_acc(c.outputOcropusGrepect, c.truthGrepect, c.outputWordReportOcropusGrepact, c.frontierPath, "wordacc", "Ocropus")
	run_acc(c.outputTesseractArgus, c.truthArgus, c.outputWordReportTesseractArgus, c.frontierPath, "wordacc", "Tesseract")
	run_acc(c.outputTesseractGrepect, c.truthGrepect, c.outputWordReportTesseractGrepect, c.frontierPath, "wordacc","Tesseract")

	combinedAcc(c.outputWordReportOcropusArgus, c.frontierPath, "wordaccsum", "WordAcc_OcropusArgus.txt")
	combinedAcc(c.outputWordReportOcropusGrepact, c.frontierPath, "wordaccsum", "WordAcc_OcropusGrepect.txt")
	combinedAcc(c.outputWordReportTesseractArgus, c.frontierPath, "wordaccsum", "WordAcc_TesseractArgus.txt")
	combinedAcc(c.outputWordReportTesseractGrepect, c.frontierPath, "wordaccsum", "WordAcc_TesseractGrepect.txt")


def main():
	completeEvaluation()
main()
