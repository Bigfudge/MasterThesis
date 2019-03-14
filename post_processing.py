import gen_vector
import word_classifier
import error_correction
import os
import constants
import sys
import glob

def process_file(plain_text, svm_input, output_file):
    gen_vector.get_training_data(constants.training_data, constants.main_db)
    gen_vector.get_input(plain_text, svm_input)
    svclassifier = word_classifier.train(constants.svm_model, constants.training_data)
    classified_words = word_classifier.predict(svm_input, svclassifier)

    output=[]
    for word in classified_words:
        if(word[1]==0):
            corr_word =error_correction.correct_word(word[0])
        else:
            corr_word= word[0]
        output.append(corr_word)

    with open(output_file, 'w') as f:
        for item in output:
            f.write("%s " % item)


def process_dir(input_dir, test, sample_size):
    count=1
    for file in os.listdir(input_dir):
        plain = input_dir+file
        svm_input= c.input
        output_dir= "./output/%s/%s"%(test,file)
        print(plain)
        if(not os.path.isfile(output_dir)):
            process_file(plain, svm_input, output_dir)
        print("Corrected page %i out of %i)" %(count, len(os.listdir(input_dir))))
        count+=1
        # if(sample_size<count):
        #     break

def remove_output(path):
    files = glob.glob(path)
    for f in files:
        print(f)
        os.remove(f)


def main():
    sample_size =0

    if('-c' in sys.argv):
        clean_run()
    if('-ss' in sys.argv):
        sample_size= 1

    remove_output('./output/OcropusArgus/*')
    remove_output('./output/OcropusGrepect/*')
    remove_output('./output/TesseractArgus/*')
    remove_output('./output/TesseractGrepect/*')

    print("Correcting text (1/4)")
    process_dir("./Evaluation-script/OCROutput/Ocropus/Argus/", "OcropusArgus",10)
    print("Correcting text (2/4)")
    process_dir("./Evaluation-script/OCROutput/Ocropus/Grepect/", "OcropusGrepect",10)
    print("Correcting text (3/4)")
    process_dir("./Evaluation-script/OCROutput/Tesseract/Argus/", "TesseractArgus",10)
    print("Correcting text (4/4)")
    process_dir("./Evaluation-script/OCROutput/Tesseract/Grepect/", "TesseractGrepect",10)

main()
