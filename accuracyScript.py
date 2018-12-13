from subprocess import call
import os
import shutil
import glob
import subprocess

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

def main():
	genOcropusArgus= "/chalmers/users/simp/MasterThesis/OCR output/Ocropus/Argus/"
	genOcropusGrepect= "/chalmers/users/simp/MasterThesis/OCR output/Ocropus/Grepect/"
	genTesseractArgus= "/chalmers/users/simp/MasterThesis/OCR output/Tesseract/Argus/"
	genTesseractGrepect= "/chalmers/users/simp/MasterThesis/OCR output/Tesseract/Grepect/"
	
	truthArgus="/chalmers/users/simp/MasterThesis/ManuelTranscript/Argus/"
	truthGrepect="/chalmers/users/simp/MasterThesis/ManuelTranscript/Grepect/"
	
	charReportOcropusArgus="/chalmers/users/simp/MasterThesis/Reports/CharAcc/Ocropus/Argus/"
	charReportOcropusGrepact="/chalmers/users/simp/MasterThesis/Reports/CharAcc/Ocropus/Grepect/"
	charReportTesseractArgus="/chalmers/users/simp/MasterThesis/Reports/CharAcc/Tesseract/Argus/"
	charReportTesseractGrepect="/chalmers/users/simp/MasterThesis/Reports/CharAcc/Tesseract/Grepect/"

	wordReportOcropusArgus="/chalmers/users/simp/MasterThesis/Reports/WordAcc/Ocropus/Argus/"
	wordReportOcropusGrepact="/chalmers/users/simp/MasterThesis/Reports/WordAcc/Ocropus/Grepect/"
	wordReportTesseractArgus="/chalmers/users/simp/MasterThesis/Reports/WordAcc/Tesseract/Argus/"
	wordReportTesseractGrepect="/chalmers/users/simp/MasterThesis/Reports/WordAcc/Tesseract/Grepect/"


	frontierPath="/chalmers/users/simp/MasterThesis/ftk-1.0/bin/Linux/"
	
	run_acc(genOcropusArgus, truthArgus, charReportOcropusArgus, frontierPath, "accuracy", "Ocropus")
	run_acc(genOcropusGrepect, truthGrepect, charReportOcropusGrepact, frontierPath, "accuracy", "Ocropus")
	run_acc(genTesseractArgus, truthArgus, charReportTesseractArgus, frontierPath, "accuracy", "Tesseract")
	run_acc(genTesseractGrepect, truthGrepect, charReportTesseractGrepect, frontierPath, "accuracy","Tesseract")
	
	combinedAcc(charReportOcropusArgus, frontierPath, "accsum", "CharAcc_OcropusArgus.txt")
	combinedAcc(charReportOcropusGrepact, frontierPath, "accsum", "CharAcc_OcropusGrepect.txt")
	combinedAcc(charReportTesseractArgus, frontierPath, "accsum", "CharAcc_TesseractArgus.txt")
	combinedAcc(charReportTesseractGrepect, frontierPath, "accsum", "CharAcc_TesseractGrepect.txt")

	run_acc(genOcropusArgus, truthArgus, wordReportOcropusArgus, frontierPath, "wordacc", "Ocropus")
	run_acc(genOcropusGrepect, truthGrepect, wordReportOcropusGrepact, frontierPath, "wordacc", "Ocropus")
	run_acc(genTesseractArgus, truthArgus, wordReportTesseractArgus, frontierPath, "wordacc", "Tesseract")
	run_acc(genTesseractGrepect, truthGrepect, wordReportTesseractGrepect, frontierPath, "wordacc","Tesseract")

	combinedAcc(wordReportOcropusArgus, frontierPath, "wordaccsum", "WordAcc_OcropusArgus.txt")
	combinedAcc(wordReportOcropusGrepact, frontierPath, "wordaccsum", "WordAcc_OcropusGrepect.txt")
	combinedAcc(wordReportTesseractArgus, frontierPath, "wordaccsum", "WordAcc_TesseractArgus.txt")
	combinedAcc(wordReportTesseractGrepect, frontierPath, "wordaccsum", "WordAcc_TesseractGrepect.txt")

 

main()
