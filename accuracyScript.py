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

def sb_eval(ocr_dir, truth_dir, source):
	pairs= get_pair(ocr_dir, truth_dir, source)
	ocr_dirs=[]
	truth_dirs=[]
	for pair in pairs:
		if(len(pair)!=2):
			continue
		ocr_file, truth_file = pair
		ocr_dirs.append(ocr_dir+ocr_file)
		truth_dirs.append(truth_dir+truth_file)
	cer, wer = sb_evaluation.main("-sb",ocr_dirs,truth_dirs)
	tot_cer=100*cer
	tot_wer=100*wer

	tmp = ocr_dir.split("/")
	return("%s_%s: CER %.2f \t WER %.2f \n"%(tmp[-2],tmp[-3],tot_cer, tot_wer))

def completeEvaluation():
	run_acc(c.genOcropusArgus, c.truthArgus, c.charReportOcropusArgus, c.frontierPath, "accuracy", "Argus")
	run_acc(c.genOcropusGrepect, c.truthGrepect, c.charReportOcropusGrepact, c.frontierPath, "accuracy", "Grepect")
	run_acc(c.genTesseractArgus, c.truthArgus, c.charReportTesseractArgus, c.frontierPath, "accuracy", "Argus")
	run_acc(c.genTesseractGrepect, c.truthGrepect, c.charReportTesseractGrepect, c.frontierPath, "accuracy","Grepect")
	run_acc(c.genABBYYArgus, c.truthArgus, c.charReportABBYYArgus, c.frontierPath, "accuracy", "Argus")
	run_acc(c.genABBYYGrepect, c.truthGrepect, c.charReportABBYYGrepect, c.frontierPath, "accuracy","Grepect")

	run_acc(c.outputOcropusArgus, c.truthArgus, c.outputCharReportOcropusArgus, c.frontierPath, "accuracy", "Argus")
	run_acc(c.outputOcropusGrepect, c.truthGrepect, c.outputCharReportOcropusGrepact, c.frontierPath, "accuracy", "Grepect")
	run_acc(c.outputTesseractArgus, c.truthArgus, c.outputCharReportTesseractArgus, c.frontierPath, "accuracy", "Argus")
	run_acc(c.outputTesseractGrepect, c.truthGrepect, c.outputCharReportTesseractGrepect, c.frontierPath, "accuracy","Grepect")
	run_acc(c.outputABBYYArgus, c.truthArgus, c.outputCharReportABBYYArgus, c.frontierPath, "accuracy", "Argus")
	run_acc(c.outputABBYYGrepect, c.truthGrepect, c.outputCharReportABBYYGrepect, c.frontierPath, "accuracy","Grepect")

	combinedAcc(c.charReportOcropusArgus, c.frontierPath, "accsum", "CharAcc_OcropusArgus.txt")
	combinedAcc(c.charReportOcropusGrepact, c.frontierPath, "accsum", "CharAcc_OcropusGrepect.txt")
	combinedAcc(c.charReportTesseractArgus, c.frontierPath, "accsum", "CharAcc_TesseractArgus.txt")
	combinedAcc(c.charReportTesseractGrepect, c.frontierPath, "accsum", "CharAcc_TesseractGrepect.txt")
	combinedAcc(c.charReportABBYYArgus, c.frontierPath, "accsum", "CharAcc_ABBYYArgus.txt")
	combinedAcc(c.charReportABBYYGrepect, c.frontierPath, "accsum", "CharAcc_ABBYYGrepect.txt")

	combinedAcc(c.outputCharReportOcropusArgus, c.frontierPath, "accsum", "Output_CharAcc_OcropusArgus.txt")
	combinedAcc(c.outputCharReportOcropusGrepact, c.frontierPath, "accsum", "Output_CharAcc_OcropusGrepect.txt")
	combinedAcc(c.outputCharReportTesseractArgus, c.frontierPath, "accsum", "Output_CharAcc_TesseractArgus.txt")
	combinedAcc(c.outputCharReportTesseractGrepect, c.frontierPath, "accsum", "Output_CharAcc_TesseractGrepect.txt")
	combinedAcc(c.outputCharReportABBYYArgus, c.frontierPath, "accsum", "Output_CharAcc_ABBYYArgus.txt")
	combinedAcc(c.outputCharReportABBYYGrepect, c.frontierPath, "accsum", "Output_CharAcc_ABBYYGrepect.txt")


	run_acc(c.genOcropusArgus, c.truthArgus, c.wordReportOcropusArgus, c.frontierPath, "wordacc", "Argus")
	run_acc(c.genOcropusGrepect, c.truthGrepect, c.wordReportOcropusGrepact, c.frontierPath, "wordacc", "Grepect")
	run_acc(c.genTesseractArgus, c.truthArgus, c.wordReportTesseractArgus, c.frontierPath, "wordacc", "Argus")
	run_acc(c.genTesseractGrepect, c.truthGrepect, c.wordReportTesseractGrepect, c.frontierPath, "wordacc","Grepect")
	run_acc(c.genABBYYArgus, c.truthArgus, c.wordReportABBYYArgus, c.frontierPath, "wordacc", "Argus")
	run_acc(c.genABBYYGrepect, c.truthGrepect, c.wordReportABBYYGrepect, c.frontierPath, "wordacc","Grepect")

	run_acc(c.outputOcropusArgus, c.truthArgus, c.outputWordReportOcropusArgus, c.frontierPath, "wordacc", "Argus")
	run_acc(c.outputOcropusGrepect, c.truthGrepect, c.outputWordReportOcropusGrepact, c.frontierPath, "wordacc", "Grepect")
	run_acc(c.outputTesseractArgus, c.truthArgus, c.outputWordReportTesseractArgus, c.frontierPath, "wordacc", "Argus")
	run_acc(c.outputTesseractGrepect, c.truthGrepect, c.outputWordReportTesseractGrepect, c.frontierPath, "wordacc","Grepect")
	run_acc(c.outputABBYYArgus, c.truthArgus, c.outputWordReportABBYYArgus, c.frontierPath, "wordacc", "Argus")
	run_acc(c.outputABBYYGrepect, c.truthGrepect, c.outputWordReportABBYYGrepect, c.frontierPath, "wordacc","Grepect")

	combinedAcc(c.wordReportOcropusArgus, c.frontierPath, "wordaccsum", "WordAcc_OcropusArgus.txt")
	combinedAcc(c.wordReportOcropusGrepact, c.frontierPath, "wordaccsum", "WordAcc_OcropusGrepect.txt")
	combinedAcc(c.wordReportTesseractArgus, c.frontierPath, "wordaccsum", "WordAcc_TesseractArgus.txt")
	combinedAcc(c.wordReportTesseractGrepect, c.frontierPath, "wordaccsum", "WordAcc_TesseractGrepect.txt")
	combinedAcc(c.wordReportABBYYArgus, c.frontierPath, "wordaccsum", "WordAcc_ABBYYArgus.txt")
	combinedAcc(c.wordReportABBYYGrepect, c.frontierPath, "wordaccsum", "WordAcc_ABBYYGrepect.txt")

	combinedAcc(c.outputWordReportOcropusArgus, c.frontierPath, "wordaccsum", "Output_WordAcc_OcropusArgus.txt")
	combinedAcc(c.outputWordReportOcropusGrepact, c.frontierPath, "wordaccsum", "Output_WordAcc_OcropusGrepect.txt")
	combinedAcc(c.outputWordReportTesseractArgus, c.frontierPath, "wordaccsum", "Output_WordAcc_TesseractArgus.txt")
	combinedAcc(c.outputWordReportTesseractGrepect, c.frontierPath, "wordaccsum", "Output_WordAcc_TesseractGrepect.txt")
	combinedAcc(c.outputWordReportABBYYArgus, c.frontierPath, "wordaccsum", "Output_WordAcc_ABBYYArgus.txt")
	combinedAcc(c.outputWordReportABBYYGrepect, c.frontierPath, "wordaccsum", "Output_WordAcc_ABBYYGrepect.txt")

def prima_evaluation(genPath, truthPath, source, outputFile):
	pairOfPaths= get_pair(genPath, truthPath, source)
	outputArray=[]
	avgW=0
	avgC=0
	count=0
	for	item in pairOfPaths:
		if(len(item)<2):
			continue
		count+=1
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
	avgW=avgW/count
	avgC=avgC/count
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
	outputArray.append("Parameters:\n")
	outputArray.append("Sample size=%s\n"%sample_size)
	outputArray.append("SVM parameters:\n\t Kernel: %s\n\t Gamma: %s\n\t C-value: %s\n\t Training data size: %s\n"
			%(svm_kernal, gamma, c_value, training_size))
	outputArray.append("SVM Performace:\n")
	# outputArray.append(word_classifier.get_performace_report(c.svm_model, c.training_data, training_size, svm_kernal, c_value, gamma))
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
	# summary.append("OcropusArgus: WordAccuracy: %s \t CharacterAccuracy: %s \n"
	# %prima_evaluation(c.genOcropusArgus, c.truthArgus, "Argus", folder_path+"/prima_OcropusArgus.txt"))
	# summary.append("OcropusGrepect: WordAccuracy: %s \t CharacterAccuracy: %s \n"
	# %prima_evaluation(c.genOcropusGrepect, c.truthGrepect, "Grepect", folder_path+"/prima_OcropusGrepect.txt"))
	# summary.append("TesseractArgus: WordAccuracy: %s \t CharacterAccuracy: %s \n"
	# %prima_evaluation(c.genTesseractArgus, c.truthArgus, "Argus", folder_path+"/prima_TesseractArgus.txt"))
	# summary.append("TesseractGrepect: WordAccuracy: %s \t CharacterAccuracy: %s \n"
	# %prima_evaluation(c.genTesseractGrepect, c.truthGrepect, "Grepect", folder_path+"/prima_TesseractGrepect.txt"))
	# summary.append("ABBYYArgus: WordAccuracy: %s \t CharacterAccuracy: %s \n"
	# %prima_evaluation(c.genTesseractArgus, c.truthArgus, "Argus", folder_path+"/prima_ABBYYArgus.txt"))
	# summary.append("ABBYYGrepect: WordAccuracy: %s \t CharacterAccuracy: %s \n\n\n"
	# %prima_evaluation(c.genABBYYGrepect, c.truthGrepect, "Grepect", folder_path+"/prima_ABBYYGrepect.txt"))

	summary.append("Post-processed output:\n")
	summary.append("OcropusArgus: WordAccuracy: %s \t CharacterAccuracy: %s \n"
	%prima_evaluation(c.outputOcropusArgus, c.truthArgus, "Argus", folder_path+"/prima_Output_OcropusArgus.txt"))
	summary.append("OcropusGrepect: WordAccuracy: %s \t CharacterAccuracy: %s \n"
	%prima_evaluation(c.outputOcropusGrepect, c.truthGrepect, "Grepect", folder_path+"/prima_Output_OcropusGrepect.txt"))
	summary.append("TesseractArgus: WordAccuracy: %s \t CharacterAccuracy: %s \n"
	%prima_evaluation(c.outputTesseractArgus, c.truthArgus, "Argus", folder_path+"/prima_Output_TesseractArgus.txt"))
	summary.append("TesseractGrepect: WordAccuracy: %s \t CharacterAccuracy: %s \n"
	%prima_evaluation(c.outputTesseractGrepect, c.truthGrepect, "Grepect", folder_path+"/prima_Output_TesseractGrepect.txt"))
	summary.append("ABBYYArgus: WordAccuracy: %s \t CharacterAccuracy: %s \n"
	%prima_evaluation(c.outputABBYYArgus, c.truthArgus, "Argus", folder_path+"/prima_Output_ABBYYArgus.txt"))
	summary.append("ABBYYGrepect: WordAccuracy: %s \t CharacterAccuracy: %s \n \n"
	%prima_evaluation(c.outputABBYYGrepect, c.truthGrepect, "Grepect", folder_path+"/prima_Output_ABBYYGrepect.txt"))

	summary.append("SB evaluation:\n")
	summary.append("OCROutput:\n")
	# summary.append(sb_eval(c.genOcropusArgus, c.truthArgus, "Argus"))
	# summary.append(sb_eval(c.genOcropusGrepect, c.truthGrepect, "Grepect"))
	# summary.append(sb_eval(c.genTesseractArgus, c.truthArgus, "Argus"))
	# summary.append(sb_eval(c.genTesseractGrepect, c.truthGrepect, "Grepect"))
	# summary.append(sb_eval(c.genABBYYArgus, c.truthArgus, "Argus"))
	# summary.append(sb_eval(c.genABBYYGrepect, c.truthGrepect, "Grepect"))
	#

	summary.append("Post-processed output:\n")
	summary.append(sb_eval(c.outputOcropusArgus, c.truthArgus, "Argus"))
	summary.append(sb_eval(c.outputOcropusGrepect, c.truthGrepect, "Grepect"))
	summary.append(sb_eval(c.outputTesseractArgus, c.truthArgus, "Argus"))
	summary.append(sb_eval(c.outputTesseractGrepect, c.truthGrepect, "Grepect"))
	summary.append(sb_eval(c.outputABBYYArgus, c.truthArgus, "Argus"))
	summary.append(sb_eval(c.outputABBYYGrepect, c.truthGrepect, "Grepect"))



	with open(folder_path+"/summary.txt", 'w') as fd:
		for line in summary:
			fd.write(line)

# main(10,'rbf',1000, 10000, 100000, 13000, 10000)
