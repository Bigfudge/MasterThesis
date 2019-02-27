import os
from glob import glob
from subprocess import call

def main(image_dir, output_dir, source, truth_dir):
    images=[]
    truth=[]
    count =1
    filenames=[]

    for file in os.listdir(image_dir):
        if file.endswith(".jpg"):
            images.append(file)
    for file in os.listdir(truth_dir):
        truth.append(file)

    for item in truth:
        for image in images:
            imagePath = image_dir+'/'+image
            ocropyFolder="%04d" % (count,)
            bookPath= '../ocropy/'+source+'/'+ocropyFolder
	
            if(source == 'grepect'):	  
                if(os.path.splitext(item)[0]==os.path.splitext(image)[0]):
		    print("PROCESSING IMAGE"+str(item))
                    ocropyGen(imagePath, source, ocropyFolder, bookPath)
                    saveOCR(bookPath, output_dir, image)
#                    count +=1
                    break

            elif(source == 'argus'):
                if(os.path.splitext(item)[0][-4:]==os.path.splitext(image)[0][-4:]):
                    print("PROCESSING IMAGE"+str(item))
		    ocropyGen(imagePath, source, ocropyFolder, bookPath)
                    saveOCR(bookPath, output_dir, image)
 #                   count +=1
                    break


def ocropyGen(imagePath, source, ocropyFolder, bookPath):
    ocroOut= '../ocropy/'+source
    call(['../ocropy/ocropus-nlbin',imagePath, '-o',ocroOut])
    call(['../ocropy/ocropus-gpageseg', bookPath+'.bin.png', '-n'])
    call(["../ocropy/ocropus-rpred", "-Q 4", "-m", "../ocropy/models/clean_natural_140420-00024000.pyrnn.gz", bookPath+'/??????.bin.png', "-n"])

def saveOCR(bookPath, output_dir, image):
    filenames=[]
    for file in os.listdir(bookPath):
            if file.endswith(".txt"):
                filenames.append(bookPath+"/"+file)
    name = os.path.splitext(image)[0]
    with open(output_dir+"/"+str(name), 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)

#main("../Images/Grepect", "./Evaluation-script/OCROutput/Ocropus/Grepect", "grepect", "./Evaluation-script/ManuelTranscript/Grepect")

main("../Images/Argus", "./Evaluation-script/OCROutput/Ocropus/Argus", "argus", "./Evaluation-script/ManuelTranscript/Argus")





