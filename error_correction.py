import xml.etree.ElementTree as ET
import csv
import os
import constants
from Levenshtein import distance

# A Dynamic Programming based Python program for edit
# distance problem
def editDistDP(word1, word2, m, n):
    str1= str(word1)
    str2 = str(word2)
    # Create a table to store results of subproblems
    dp = [[0 for x in range(n+1)] for x in range(m+1)]

    # Fill d[][] in bottom up manner
    for i in range(m+1):
        for j in range(n+1):

            # If first string is empty, only option is to
            # insert all characters of second string
            if i == 0:
                dp[i][j] = j    # Min. operations = j

            # If second string is empty, only option is to
            # remove all characters of second string
            elif j == 0:
                dp[i][j] = i    # Min. operations = i

            # If last characters are same, ignore last char
            # and recur for remaining string
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]

            # If last character are different, consider all
            # possibilities and find minimum
            else:
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert
                                   dp[i-1][j],        # Remove
                                   dp[i-1][j-1])    # Replace

    return dp[m][n]

def old_correct_word(word):
    freq=[]
    with open('data/word_freq.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        freq = list(reader)
    edit_dist=1
    candidates=[]

    while (edit_dist < len(str(word))+2 or edit_dist <= 8):
        for candidate in freq:
            min_word_len = len(candidate[0])-edit_dist
            max_word_len = len(candidate[0])+edit_dist

            if(not(min_word_len <= len(str(word)) <= max_word_len)):
                continue
            if (editDistDP(word,candidate[0],len(str(word)), len(candidate[0])) == edit_dist):
                candidates.append(candidate)

        if(len(candidates)>0):
            #Select candidate with greatest frequency
            winning_candidate=max(candidates, key=lambda x: x[1])
            return winning_candidate[0]
        else:
            edit_dist+=1
    #If no candidate is found the original word is returned
    return(word)

def extract_words(xml_files):
    all_words=[]
    for file in xml_files:
        tree = ET.parse(file)
        root = tree.getroot()
        for text in root:
            for paragraph in text:
                for sentence in paragraph:
                    for word in sentence:
                        all_words.append(str(word.text))

    return(all_words)

def correct_word(word):
    freq=[]
    with open('data/word_freq.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        freq = list(reader)
    edit_dist=1
    candidates=[]
    edit_distances=[]

    for can in freq:
        edit_distances.append([can,distance(can[0],str(word))])
    while (edit_dist < len(str(word))+2 or edit_dist <= 8):
        for item in edit_distances:
            if(item[0][1]==edit_dist):
                candidates.append(item[0])
        if(len(candidates)>0):
            #Select candidate with greatest frequency
            winning_candidate=max(candidates, key=lambda x: x[1])
            return winning_candidate[0]
        else:
            edit_dist+=1
    #If no candidate is found the original word is returned
    return(word)

def calc_freq(words):
    freq = [[]]
    if (not os.path.isfile(constants.word_freq_path)):
        for word in words:
            count = 1
            for dup in words:
                if(word==dup):
                    words.remove(dup)
                    count+=1
            freq.append([word,count])
        with open(constants.word_freq_path, 'w') as csvFile:
            writer=csv.writer(csvFile)
            writer.writerows(freq)
    else:
        with open(constants.word_freq_path, 'r') as readFile:
            reader = csv.reader(readFile)
            freq = list(reader)
    return freq

def main():
    all_words = extract_words([constants.corpus_lag,constants.corpus_tank])
    print('Words extracted from .xml')
    word_freq = calc_freq(all_words)
    print('Frequencies calculated')

