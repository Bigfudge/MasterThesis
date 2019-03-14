import gen_vector
import word_classifier
import error_correction
import os
import constants as c
import sys
import glob
import alternative_word_classifier

def process_file(plain_text, svm_input, output_file):
    gen_vector.get_training_data(c.training_data, c.main_db)
    gen_vector.get_input(plain_text, svm_input)
    svclassifier = word_classifier.train(c.svm_model, c.training_data)
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

def remove_output(path):
    files = glob.glob(path)
    for f in files:
        print(f)
        os.remove(f)

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
        if(sample_size):
            if(sample_size<count):
                break

def clean_run():
    if(os.path.exists(c.svm_model)):
        os.remove(c.svm_model)

    if(os.path.exists(c.main_db)):
        os.remove(c.main_db)

    if(os.path.exists(c.input)):
        os.remove(c.input)

    if(os.path.exists(c.training_data)):
        os.remove(c.training_data)

    if(os.path.exists(c.word_freq_path)):
        os.remove(c.word_freq_path)

    if(os.path.exists(c.trigrams_db)):
        os.remove(c.trigrams_db)


def main():
    sample_size =0

    if('-c' in sys.argv):
        clean_run()
    if('-ss' in sys.argv):
        sample_size= 30

    remove_output('./output/OcropusArgus/*')
    remove_output('./output/OcropusGrepect/*')
    remove_output('./output/TesseractArgus/*')
    remove_output('./output/TesseractGrepect/*')


    print("Correcting text (1/4)")
    process_dir("./Evaluation-script/OCROutput/Ocropus/Argus/", "OcropusArgus",sample_size)
    print("Correcting text (2/4)")
    process_dir("./Evaluation-script/OCROutput/Ocropus/Grepect/", "OcropusGrepect",sample_size)
    print("Correcting text (3/4)")
    process_dir("./Evaluation-script/OCROutput/Tesseract/Argus/", "TesseractArgus",sample_size)
    print("Correcting text (4/4)")
    process_dir("./Evaluation-script/OCROutput/Tesseract/Grepect/", "TesseractGrepect",sample_size)

main()
