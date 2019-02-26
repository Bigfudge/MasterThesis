import os
from glob import glob
from subprocess import call

def gen():
    imagePaths=[]
    truthPaths=[]
    index=[]
    for file in os.listdir("../Images/Grepect/"):
        imagePaths.append(os.path.splitext(file)[0])
    for file in os.listdir("./Evaluation-script/ManuelTranscript/Grepect"):
	truthPaths.append(os.path.splitext(file)[0])
    for item in truthPaths:
	index.append(imagePaths.index(item))
    for item in index:
	#print item
	test= "%04d" % (item,)
	path= '../ocropy/Grepect/'+str(test)+'/??????.bin.png'
	call(["../ocropy/ocropus-rpred", "-Q 4", "-m", "../ocropy/models/clean_natural_140420-00024000.pyrnn.gz", path, "-n"])

def argus(image_dir, input_dir,output_dir, truth_dir):
    truth =[]
    images =[]
    index =[]
    filenames=[]
    for file in os.listdir(truth_dir):
        truth.append(os.path.splitext(file)[0][-4:])
    for file in os.listdir(image_dir):
        images.append(os.path.splitext(file)[0][-4:])
    for item in truth:
        index.append(images.index(item))
    
    for item in index:
	test= "%04d" % (item,)
        folder = str(input_dir)+'/'+str(test)
        for file in os.listdir(folder):
            if file.endswith(".txt"):
                filenames.append(folder+"/"+file)
	print(images[item])
        with open(output_dir+"/"+str(images[item]), 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)


def grepect(image_dir, input_dir,output_dir, truth_dir):
    truth =[]
    images =[]
    index =[]
    filenames=[]
    for file in os.listdir(truth_dir):
	truth.append(os.path.splitext(file)[0])
    for file in os.listdir(image_dir):
	images.append(os.path.splitext(file)[0])
    for item in truth:
        index.append(images.index(item))
    
    for item in index:
	test= "%04d" % (item,)
	folder = str(input_dir)+'/'+str(test)
	if(not os.path.isdir(folder)):
	    continue
	for file in os.listdir(folder):
            if file.endswith(".txt"):
                filenames.append(folder+"/"+file)
	print(images[item])
	with open(output_dir+"/"+str(images[item]), 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)

argus("../Images/Argus", "../ocropy/Argus", "./Evaluation-script/OCROutput/Ocropus/Argus","./Evaluation-script/ManuelTranscript/Argus")
grepect("../Images/Grepect", "../ocropy/Grepect", "./Evaluation-script/OCROutput/Ocropus/Grepect","./Evaluation-script/ManuelTranscript/Grepect")
#gen()
