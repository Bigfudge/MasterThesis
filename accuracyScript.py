from subprocess import call
import os
import shutil


def	charAcc(genPath, truthPath, reportPath, frontierPath, command, engine):
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
		call([frontierPath+command,truthPath+item[1], genPath+item[0],reportPath+"report_"+str(count)])
		count += 1

def main():
	genOcropusArgus= "/chalmers/users/simp/MasterThesis/OCR output/Ocropus/Argus/"
	genOcropusGrepect= "/chalmers/users/simp/MasterThesis/OCR output/Ocropus/Grepect/"
	genTesseractArgus= "/chalmers/users/simp/MasterThesis/OCR output/Tesseract/Argus/"
	genTesseractGrepect= "/chalmers/users/simp/MasterThesis/OCR output/Tesseract/Grepect/"
	
	truthArgus="/chalmers/users/simp/MasterThesis/ManuelTranscript/Argus/"
	truthGrepect="/chalmers/users/simp/MasterThesis/ManuelTranscript/Grepect/"
	
	reportOcropusArgus="/chalmers/users/simp/MasterThesis/Reports/Ocropus/Argus/"
	reportOcropusGrepact="/chalmers/users/simp/MasterThesis/Reports/Ocropus/Grepect/"
	reportTesseractArgus="/chalmers/users/simp/MasterThesis/Reports/Tesseract/Argus/"
	reportTesseractGrepect="/chalmers/users/simp/MasterThesis/Reports/Tesseract/Grepect/"
	frontierPath="/chalmers/users/simp/MasterThesis/ftk-1.0/bin/Linux/"
	
	charAcc(genOcropusArgus, truthArgus, reportOcropusArgus, frontierPath, "accuracy", "Ocropus")
	charAcc(genOcropusGrepect, truthGrepect, reportOcropusGrepact, frontierPath, "accuracy", "Ocropus")
	charAcc(genTesseractArgus, truthArgus, reportTesseractArgus, frontierPath, "accuracy", "Tesseract")
	charAcc(genTesseractGrepect, truthGrepect, reportTesseractGrepect, frontierPath, "accuracy","Tesseract")

	

main()
