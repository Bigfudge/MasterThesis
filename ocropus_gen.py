import os
from glob import glob
from subprocess import call


def main(input_dir,output_dir):
    dirs = [x[0] for x in os.walk(input_dir)]
    count=0
    filenames = []
    for folder in dirs:
        for file in os.listdir(folder):
            if file.endswith(".txt"):
                filenames.append(folder+"/"+file)
        with open(output_dir+"/"+str(count), 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)
        filenames=[]
        count+=1

main("/Users/simonpersson/Github/ocropy/Argus", "/Users/simonpersson/Github/MasterThesis/Evaluation-script/OCROutput/Ocropus/Argus")
