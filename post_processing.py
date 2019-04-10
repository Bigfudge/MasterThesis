import gen_vector
import word_classifier
import error_correction
import os
import constants as c
import sys
import glob
import accuracyScript

def process_file(plain_text,output_file, db_size, training_size, svm_kernal, c_value, gamma,word_freq_size):
    error_correction.calc_freq(word_freq_size)
    gen_vector.get_training_data(c.training_data, c.main_db,db_size)
    gen_vector.get_input(plain_text, c.input)
    svclassifier = word_classifier.train(c.svm_model, c.training_data,
                    training_size, svm_kernal, c_value,gamma)
    classified_words = word_classifier.predict(c.input, svclassifier)

    output=[]
    for word in classified_words:
        if(word[1]==0):
            corr_word =error_correction.updated_correct_word(word[0])
        else:
            corr_word= word[0]
        if isinstance(corr_word, (list,)):
            for word in corr_word:
                output.append(word)
        else:
            output.append(corr_word)

    with open(output_file, 'w') as f:
        for item in output:
            f.write("%s " % item)

def remove_output(path):
    files = glob.glob(path)
    for f in files:
        print(f)
        os.remove(f)

def process_dir(input_dir, test, sample_size, db_size, training_size,
                svm_kernal, c_value, gamma,word_freq_size):
    count=1
    for file in os.listdir(input_dir):
        plain = input_dir+file
        output_dir= "./output/%s/%s"%(test,file)
        print(plain)
        if(not os.path.isfile(output_dir)):
            process_file(plain, output_dir, db_size, training_size,
                            svm_kernal, c_value, gamma,word_freq_size)
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

    if(os.path.exists(c.trigrams_path)):
        os.remove(c.trigrams_path)


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

    db_size=0
    training_size=50000
    svm_kernal="rbf"
    c_value=1.1
    gamma=1.3
    word_freq_size=20

    print("Correcting text (1/4)")
    process_dir("./Evaluation-script/OCROutput/Ocropus/Argus/", "OcropusArgus",sample_size, db_size, training_size, svm_kernal, c_value, gamma,word_freq_size)
    print("Correcting text (2/4)")
    process_dir("./Evaluation-script/OCROutput/Ocropus/Grepect/", "OcropusGrepect",sample_size, db_size, training_size, svm_kernal, c_value, gamma,word_freq_size)
    print("Correcting text (3/4)")
    process_dir("./Evaluation-script/OCROutput/Tesseract/Argus/", "TesseractArgus",sample_size, db_size, training_size, svm_kernal, c_value, gamma,word_freq_size)
    print("Correcting text (4/4)")
    process_dir("./Evaluation-script/OCROutput/Tesseract/Grepect/", "TesseractGrepect",sample_size, db_size, training_size, svm_kernal, c_value, gamma,word_freq_size)

    accuracyScript.main(sample_size, svm_kernal, gamma, c_value,
    		training_size, db_size, word_freq_size)

main()
