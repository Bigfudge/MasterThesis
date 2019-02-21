from subprocess import call
import os

def main(input_dir, output):
    for file in os.listdir(input_dir):
        image = input_dir+file
        out= output+os.path.splitext(file)[0]
        print(out)
        call(["tesseract", image, out,"-l", "swe"])

main("./Images/Argus/", "./Evaluation-script/OCROutput/Tesseract/Argus/")
main("./Images/Grepect/", "./Evaluation-script/OCROutput/Tesseract/Grepect/")
