from subprocess import call
import os

def argus(input_dir, output, truthPath):
    truth=[]
    for file in os.listdir(truthPath):
	truth.append(os.path.splitext(file)[0][-4:])
    print(truth)
    for file in os.listdir(input_dir):
	if(os.path.splitext(file)[0][-4:] not in truth):
	    print("skip")
	    continue
        image = input_dir+file
        out=output+os.path.splitext(file)[0]
        print(out)
        call(["tesseract", image, out,"-l", "swe"])

def grepect(input_dir, output, truthPath):
    truth=[]
    for file in os.listdir(truthPath):
        truth.append(os.path.splitext(file)[0])
    print(truth)
    for file in os.listdir(input_dir):
        if(os.path.splitext(file)[0]not in truth):
            print("skip")
            continue
        image = input_dir+file
        out=output+os.path.splitext(file)[0]
        print(out)
        call(["tesseract", image, out,"-l", "swe"])


argus("../Images/Argus/", "./Evaluation-script/OCROutput/Tesseract/Argus/", "./Evaluation-script/ManuelTranscript/Argus")
grepect("../Images/Grepect/", "./Evaluation-script/OCROutput/Tesseract/Grepect/", "./Evaluation-script/ManuelTranscript/Grepect")
