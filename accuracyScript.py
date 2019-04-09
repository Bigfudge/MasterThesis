#!/bin/sh
from subprocess import call
import os
import shutil
import glob
import subprocess
import constants as c
import sb_evaluation
import datetime
import word_classifier

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

def prima_evaluation(genPath, truthPath, source, outputFile):
	pairOfPaths= get_pair(genPath, truthPath, source)
	outputArray=[]
	avgW=0
	avgC=0
	for	item in pairOfPaths:
		if(len(item)<2):
			continue

		commandW = ["java","-jar",c.primaPath,"-gt-text",truthPath+item[1],"-res-text",genPath+item[0],
				"-method", "WordAccuracy"]
		word = subprocess.Popen(commandW,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		outputWord, error = word.communicate()

		commandC = ["java","-jar",c.primaPath,"-gt-text",truthPath+item[1],"-res-text",genPath+item[0],
				"-method", "CharacterAccuracy"]
		char = subprocess.Popen(commandC,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		outputChar, error = char.communicate()

		name = item[0]
		wAcc= str(outputWord).split(',')[2][1:-1]
		cAcc=str(outputChar).split(',')[2][1:-5]
		avgW+=float(wAcc)
		avgC+=float(cAcc)
		outString="%s \t WordAccuracy: %s \t CharacterAccuracy: %s \n"%(name,wAcc,cAcc)
		outputArray.append(outString)
		if error:
			print("ERROR", error)
	avgW=avgW/len(pairOfPaths)
	avgC=avgC/len(pairOfPaths)
	avgString= "Average:\t WordAccuracy: %s \t CharacterAccuracy: %s \n"%(avgW,avgC)
	print(avgString)
	outputArray= [avgString]+outputArray
	with open(outputFile, 'w') as fd:
		for line in outputArray:
			fd.write(line)
	return avgW, avgC

def make_conf_file(outputFile, sample_size, svm_kernal, gamma, c_value,
					training_size, db_size, word_freq_size):
	outputArray=[]
	outputArray.append("Parameters")
	outputArray.append("Sample size=%s\n"%sample_size)
	outputArray.append("SVM parameters:\n\t Kernel: %s\n\t Gamma: %s\n\t C-value: %s\n\t Training data size: %s\n"
			%(svm_kernal, gamma, c_value, training_size))
	outputArray.append("SVM Performace:\n")
	outputArray.append(word_classifier.get_performace_report(c.svm_model, c.training_data, training_size))
	outputArray.append("Database_size: %s \n Word_frequency size: %s"%(db_size,word_freq_size))
	with open(outputFile, 'w') as fd:
		for line in outputArray:
			fd.write(line)


def main(sample_size, svm_kernal, gamma, c_value,
		training_size, db_size, word_freq_size):
		#completeEvaluation()
		#print_sb_eval_gen("gen_SB_Evaluation.txt")
		#print_sb_eval_output("output_SB_Evaluation.txt")
	summary=[]
	now = datetime.datetime.now()
	folder_name= now.strftime("%Y-%m-%d %H:%M")
	folder_path="./Evaluation-reports/%s"%(folder_name)

	os.mkdir(folder_path)
	make_conf_file(folder_path+"/configuration.txt", sample_size, svm_kernal,
	 				gamma, c_value, training_size, db_size, word_freq_size)

	summary.append("SUMMARY:\n")
	summary.append("PrimA evaluation:\n")
	summary.append("OCROutput:\n")
	summary.append("OcropusArgus: WordAccuracy: %s \t CharacterAccuracy: %s \n"
	%prima_evaluation(c.genOcropusArgus, c.truthArgus, "Argus", folder_path+"/prima_OcropusArgus.txt"))
	summary.append("OcropusGrepect: WordAccuracy: %s \t CharacterAccuracy: %s \n"
	%prima_evaluation(c.genOcropusGrepect, c.truthGrepect, "Grepect", folder_path+"/prima_OcropusGrepect.txt"))
	summary.append("TesseractArgus: WordAccuracy: %s \t CharacterAccuracy: %s \n"
	%prima_evaluation(c.genTesseractArgus, c.truthArgus, "Argus", folder_path+"/prima_TesseractArgus.txt"))
	summary.append("TesseractGrepect: WordAccuracy: %s \t CharacterAccuracy: %s \n\n\n"
	%prima_evaluation(c.genTesseractGrepect, c.truthGrepect, "Grepect", folder_path+"/prima_TesseractGrepect.txt"))

	summary.append("Post-processed output:\n")
	summary.append("OcropusArgus: WordAccuracy: %s \t CharacterAccuracy: %s \n"
	%prima_evaluation(c.outputOcropusArgus, c.truthArgus, "Argus", folder_path+"/prima_Output_OcropusArgus.txt"))
	summary.append("OcropusGrepect: WordAccuracy: %s \t CharacterAccuracy: %s \n"
	%prima_evaluation(c.outputOcropusGrepect, c.truthGrepect, "Grepect", folder_path+"/prima_Output_OcropusGrepect.txt"))
	summary.append("TesseractArgus: WordAccuracy: %s \t CharacterAccuracy: %s \n"
	%prima_evaluation(c.outputTesseractArgus, c.truthArgus, "Argus", folder_path+"/prima_Output_TesseractArgus.txt"))
	summary.append("TesseractGrepect: WordAccuracy: %s \t CharacterAccuracy: %s \n"
	%prima_evaluation(c.outputTesseractGrepect, c.truthGrepect, "Grepect", folder_path+"/prima_Output_TesseractGrepect.txt"))

	with open(folder_path+"/summary.txt", 'w') as fd:
		for line in summary:
			fd.write(line)

# main()
