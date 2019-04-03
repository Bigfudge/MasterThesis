#!/bin/sh
from subprocess import call
import os
import shutil
import glob
import subprocess
import constants as c
import sb_evaluation

def get_pair(genPath, truthPath, source):
	pairOfPaths= []
	for gen in os.listdir(genPath):
		pairOfPaths.append([gen])
	if(source=="Grepect"):
		for truth in os.listdir(truthPath):
			for	match in pairOfPaths:
				gen = match[0]
				if(os.path.splitext(gen)[0]==os.path.splitext(truth)[0]):

					match.append(truth)
	elif(source=="Argus"):
		for truth in os.listdir(truthPath):
			for	match in pairOfPaths:
				gen = match[0]
				if(os.path.splitext(gen)[0][-4:]==os.path.splitext(truth)[0][-4:]):

					match.append(truth)
	else:
		print("Wrong engine")
	return pairOfPaths

def	run_acc(genPath, truthPath, reportPath, frontierPath, command, source):
	pairOfPaths= get_pair(genPath, truthPath, source)
	count=0
	if len(os.listdir(reportPath) ) != 0:
		os.system('rm ' + reportPath+"*")
	for	item in pairOfPaths:
		if(len(item)<2):
			continue
		call([frontierPath+command,truthPath+item[1],genPath+item[0],
				reportPath+"accuracy_report_"+str(count)])

		count += 1

def	combinedAcc(reportPath, frontierPath, command, outputFile):
	all_reports = [report for report in glob.glob(reportPath + '/*')]
	command = [frontierPath+command] + all_reports
	p = subprocess.Popen(command,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = p.communicate()
	if error:
		print("ERROR", error)
	with open(outputFile, 'w') as fd:
		fd.write(output)

def sb_eval(genPath, truthPath, source):
	pairOfPaths= get_pair(genPath, truthPath, source)
	tot_cer=0
	tot_wer=0
	count =1
	for item in pairOfPaths:
		if(count>30):
			break
		if len(item)<2:
			continue
		print(count)
		cer, wer = sb_evaluation.main("-sb",[genPath+item[0]],[truthPath+item[1]])
		tot_cer+=100*(1-cer)
		tot_wer+=100*(1-wer)
		count+=1


	tmp = genPath.split("/")
	return("%s_%s: CER %.2f \t WER %.2f \n"%(tmp[-2],tmp[-3],tot_cer/count, tot_wer/count))

def print_sb_eval_gen(output_file):
	lines = []
	lines.append(sb_eval(c.genOcropusArgus, c.truthArgus, "Argus"))
	lines.append(sb_eval(c.genOcropusGrepect, c.truthGrepect, "Grepect"))
	lines.append(sb_eval(c.genTesseractArgus, c.truthArgus, "Argus"))
	lines.append(sb_eval(c.genTesseractGrepect, c.truthGrepect, "Grepect"))
	with open(output_file, 'w') as fd:
		for line in lines:
			fd.write(line)

def print_sb_eval_output(output_file):
	lines = []
	lines.append(sb_eval(c.outputOcropusArgus, c.truthArgus, "Argus"))
	lines.append(sb_eval(c.outputOcropusGrepect, c.truthGrepect, "Grepect"))
	lines.append(sb_eval(c.outputTesseractArgus, c.truthArgus, "Argus"))
	lines.append(sb_eval(c.outputTesseractGrepect, c.truthGrepect, "Grepect"))
	with open(output_file, 'w') as fd:
		for line in lines:
			fd.write(line)

def completeEvaluation():
	run_acc(c.genOcropusArgus, c.truthArgus, c.charReportOcropusArgus, c.frontierPath, "accuracy", "Argus")
	run_acc(c.genOcropusGrepect, c.truthGrepect, c.charReportOcropusGrepact, c.frontierPath, "accuracy", "Grepect")
	run_acc(c.genTesseractArgus, c.truthArgus, c.charReportTesseractArgus, c.frontierPath, "accuracy", "Argus")
	run_acc(c.genTesseractGrepect, c.truthGrepect, c.charReportTesseractGrepect, c.frontierPath, "accuracy","Grepect")

	run_acc(c.outputOcropusArgus, c.truthArgus, c.outputCharReportOcropusArgus, c.frontierPath, "accuracy", "Argus")
	run_acc(c.outputOcropusGrepect, c.truthGrepect, c.outputCharReportOcropusGrepact, c.frontierPath, "accuracy", "Grepect")
	run_acc(c.outputTesseractArgus, c.truthArgus, c.outputCharReportTesseractArgus, c.frontierPath, "accuracy", "Argus")
	run_acc(c.outputTesseractGrepect, c.truthGrepect, c.outputCharReportTesseractGrepect, c.frontierPath, "accuracy","Grepect")


	combinedAcc(c.charReportOcropusArgus, c.frontierPath, "accsum", "CharAcc_OcropusArgus.txt")
	combinedAcc(c.charReportOcropusGrepact, c.frontierPath, "accsum", "CharAcc_OcropusGrepect.txt")
	combinedAcc(c.charReportTesseractArgus, c.frontierPath, "accsum", "CharAcc_TesseractArgus.txt")
	combinedAcc(c.charReportTesseractGrepect, c.frontierPath, "accsum", "CharAcc_TesseractGrepect.txt")

	combinedAcc(c.outputCharReportOcropusArgus, c.frontierPath, "accsum", "Output_CharAcc_OcropusArgus.txt")
	combinedAcc(c.outputCharReportOcropusGrepact, c.frontierPath, "accsum", "Output_CharAcc_OcropusGrepect.txt")
	combinedAcc(c.outputCharReportTesseractArgus, c.frontierPath, "accsum", "Output_CharAcc_TesseractArgus.txt")
	combinedAcc(c.outputCharReportTesseractGrepect, c.frontierPath, "accsum", "Output_CharAcc_TesseractGrepect.txt")


	run_acc(c.genOcropusArgus, c.truthArgus, c.wordReportOcropusArgus, c.frontierPath, "wordacc", "Argus")
	run_acc(c.genOcropusGrepect, c.truthGrepect, c.wordReportOcropusGrepact, c.frontierPath, "wordacc", "Grepect")
	run_acc(c.genTesseractArgus, c.truthArgus, c.wordReportTesseractArgus, c.frontierPath, "wordacc", "Argus")
	run_acc(c.genTesseractGrepect, c.genTesseractGrepect, c.wordReportTesseractGrepect, c.frontierPath, "wordacc","Grepect")

	run_acc(c.outputOcropusArgus, c.truthArgus, c.outputWordReportOcropusArgus, c.frontierPath, "wordacc", "Argus")
	run_acc(c.outputOcropusGrepect, c.truthGrepect, c.outputWordReportOcropusGrepact, c.frontierPath, "wordacc", "Grepect")
	run_acc(c.outputTesseractArgus, c.truthArgus, c.outputWordReportTesseractArgus, c.frontierPath, "wordacc", "Argus")
	run_acc(c.outputTesseractGrepect, c.truthGrepect, c.outputWordReportTesseractGrepect, c.frontierPath, "wordacc","Grepect")

	combinedAcc(c.wordReportOcropusArgus, c.frontierPath, "wordaccsum", "WordAcc_OcropusArgus.txt")
	combinedAcc(c.wordReportOcropusGrepact, c.frontierPath, "wordaccsum", "WordAcc_OcropusGrepect.txt")
	combinedAcc(c.wordReportTesseractArgus, c.frontierPath, "wordaccsum", "WordAcc_TesseractArgus.txt")
	combinedAcc(c.wordReportTesseractGrepect, c.frontierPath, "wordaccsum", "WordAcc_TesseractGrepect.txt")

	combinedAcc(c.outputWordReportOcropusArgus, c.frontierPath, "wordaccsum", "Output_WordAcc_OcropusArgus.txt")
	combinedAcc(c.outputWordReportOcropusGrepact, c.frontierPath, "wordaccsum", "Output_WordAcc_OcropusGrepect.txt")
	combinedAcc(c.outputWordReportTesseractArgus, c.frontierPath, "wordaccsum", "Output_WordAcc_TesseractArgus.txt")
	combinedAcc(c.outputWordReportTesseractGrepect, c.frontierPath, "wordaccsum", "Output_WordAcc_TesseractGrepect.txt")

	#print_sb_eval("SB_Evaluation.txt")

def outputEvaluation():
	run_acc(c.outputOcropusArgus, c.truthArgus, c.outputCharReportOcropusArgus, c.frontierPath, "accuracy", "Argus")
	run_acc(c.outputOcropusGrepect, c.truthGrepect, c.outputCharReportOcropusGrepact, c.frontierPath, "accuracy", "Grepect")
	run_acc(c.outputTesseractArgus, c.truthArgus, c.outputCharReportTesseractArgus, c.frontierPath, "accuracy", "Argus")
	run_acc(c.outputTesseractGrepect, c.truthGrepect, c.outputCharReportTesseractGrepect, c.frontierPath, "accuracy","Grepect")

	combinedAcc(c.outputCharReportOcropusArgus, c.frontierPath, "accsum", "Output_CharAcc_OcropusArgus.txt")
	combinedAcc(c.outputCharReportOcropusGrepact, c.frontierPath, "accsum", "Output_CharAcc_OcropusGrepect.txt")
	combinedAcc(c.outputCharReportTesseractArgus, c.frontierPath, "accsum", "Output_CharAcc_TesseractArgus.txt")
	combinedAcc(c.outputCharReportTesseractGrepect, c.frontierPath, "accsum", "Output_CharAcc_TesseractGrepect.txt")

	run_acc(c.outputOcropusArgus, c.truthArgus, c.outputWordReportOcropusArgus, c.frontierPath, "wordacc", "Argus")
	run_acc(c.outputOcropusGrepect, c.truthGrepect, c.outputWordReportOcropusGrepact, c.frontierPath, "wordacc", "Grepect")
	run_acc(c.outputTesseractArgus, c.truthArgus, c.outputWordReportTesseractArgus, c.frontierPath, "wordacc", "Argus")
	run_acc(c.outputTesseractGrepect, c.truthGrepect, c.outputWordReportTesseractGrepect, c.frontierPath, "wordacc","Grepect")

	combinedAcc(c.outputWordReportOcropusArgus, c.frontierPath, "wordaccsum", "WordAcc_OcropusArgus.txt")
	combinedAcc(c.outputWordReportOcropusGrepact, c.frontierPath, "wordaccsum", "WordAcc_OcropusGrepect.txt")
	combinedAcc(c.outputWordReportTesseractArgus, c.frontierPath, "wordaccsum", "WordAcc_TesseractArgus.txt")
	combinedAcc(c.outputWordReportTesseractGrepect, c.frontierPath, "wordaccsum", "WordAcc_TesseractGrepect.txt")


def main():
	completeEvaluation()
	#print_sb_eval_gen("gen_SB_Evaluation.txt")
	#print_sb_eval_output("output_SB_Evaluation.txt")

main()
