import gen_vector
import word_classifier
import error_correction

def process_file(plain_text, svm_input, output_file):
    gen_vector.get_training_data("data/input_vector.csv", "data/data_set.db")
    gen_vector.get_input(plain_text, svm_input)

    svclassifier = word_classifier.train("models/finalized_model.sav", "data/input_vector.csv")
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
            f.write("%s\n" % item)

process_file("./Evaluation-script/OCROutput/Ocropus/Argus/ed_pg_a0002_ocropus_twomodel.txt",
            "data/input.csv",
            "output.txt")
