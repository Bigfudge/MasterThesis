import numpy as np

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
           'n','o','p','q','r','s','t','u','v','w','x','y','z','å','ä','ö', ' ']

def make_noise(word, threshold):
    noisy_word=[]
    wordList= list(word)
    i=0
    while i <len(wordList):
        random = np.random.uniform(0,1,1)

        # Most characters will be correct since the threshold value is high
        if random < threshold:
            noisy_word.append(wordList[i])
        else:
            new_random = np.random.uniform(0,1,1)
            if new_random > 0.67:
                if i == (len(wordList) - 1):
                    # If last character in sentence, it will not be typed
                    continue
                else:
                    # if any other character, swap order with following character
                    noisy_word.append(wordList[i+1])
                    noisy_word.append(wordList[i])
                    i += 1
            # ~33% chance an extra lower case letter will be added to the sentence
            elif new_random < 0.33:
                random_letter = np.random.choice(letters, 1)[0]
                noisy_word.append(random_letter)
                noisy_word.append(wordList[i])
            # ~33% chance a character will not be typed
            else:
                pass
        i += 1
    output = ''.join(noisy_word)

    if(output==word):
        output = make_noise(word, threshold)
    return(output)

# print(make_noise("aaabbbcccddddeee",0.9))
