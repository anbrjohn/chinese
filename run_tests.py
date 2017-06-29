import time
import numpy as np

 
def get_age(word, data_dic, constant=1, rate=1.2):
    # Calculates age factor
    last_time = data_dic[word][1]
    current_time = int(time.time())
    day_length = 60*60*24
    if last_time > 0:
        # How many days since last repetition
        day_interval = int((current_time - last_time) / day_length) 
    else: # For new words, default to 6 months
        day_interval = 30 * 6
    age_factor = constant * rate ** day_interval
    return age_factor


def get_progress(word, data_dic, constant=1.2, rate=1.2):
    # To update progress value, set correct or incorrect argument to True
    progress_value = data_dic[word][0]
    progress_factor = constant * rate ** (-progress_value)
    return progress_factor


def weighted_wordlist(data_dic):
    words = []
    weights = []
    for word in data_dic:
        words += [word]
        progress = get_progress(word, data_dic)
        age = get_age(word, data_dic)
        weights += [progress*age]
    total = sum(weights)
    # Normalize to sum to 1
    weights = [item/total for item in weights]
    return words, weights


def initialize(wordlist_file, results_file):
    timestamp = time.time()
    entries = {}
    with open(wordlist_file) as f:
        for line in f:
            if len(line) > 0:
                data = (line.strip().split("\t")) #hanzi, pinyin, tone, english
                entries[data[0]] = (data[1], data[2], data[3])
    hanzi_data = {}
    pinyin_data = {}
    tone_data = {}
    english_data = {}
    with open(results_file) as f:
        for line in f:
            if len(line) > 0:
                if line[0] != "*":
                    data = line.strip().split("\t")
                    # The chinese word, the key for the dictionary
                    word = data[0]
                    # Convert everything but first entry to a float
                    data = [float(item) for item in data[1:]]
                    # key: (percentage right, date last tested)
                    hanzi_data[word] = [data[0], data[1]]
                    pinyin_data[word] = [data[2], data[3]]
                    tone_data[word] = [data[4], data[5]]
                    english_data[word] = [data[6], data[7]]
    # For words newly added to wordlist but not yet in results, 
    # add to results file and relevant dictionaries
    with open(results_file, "a") as f:
        for word in entries:
            if word not in hanzi_data:
                line = word+"\t0" * 8 + "\n"
                f.write(line)
                hanzi_data[word] = [0, 0]
                pinyin_data[word] = [0, 0]
                tone_data[word] = [0, 0]
                english_data[word] = [0, 0]
    return entries, hanzi_data, pinyin_data, tone_data, english_data

            
def test_tones(question_num, question_format="hz", color=True): # number of questions to do
    print("Enter tones for the following:")
    words, weights = weighted_wordlist(tone_data) ###
    quiz_words = np.random.choice(words, size=question_num, p=weights, replace=False)
    i = 0
    for qw in quiz_words:
        if question_format == "hz": # use hanzi
            tones = input(str(i+1) + ") " + qw + " : ")
        else: # use pinyin
            pinyin = entries[qw][0]
            tones = input(str(i+1) + ") " + pinyin + " : ")
        tones = [ch for ch in tones if ch.isdigit()]
        tones = "".join(tones)
        correct = entries[qw][1] ###
        if tones == correct:
            if color:
                colored = colorize(qw, tones)
                print("Correct!\t", colored, "\t", entries[qw][0])
            else:
                print("Correct!\t", tones, "\t", entries[qw][0])
            tone_data[qw][0] += 1 ###
        else:
            if color:
                colored = colorize(qw, correct)
                print("Incorect:\t", colored, "\t", correct, "\t", entries[qw][0])
            else:
                print("Incorect:\t", correct, "\t", entries[qw][0])
            tone_data[qw][0] -= 1 ###
        tone_data[qw][1] = int(time.time()) ###
        print("\n")
        i += 1


def colorize(word, tones):
    # (white), blue, yellow, green, red, and white background colors
    colors = ['', '\x1b[1;31;46m', '\x1b[1;31;43m', '\x1b[0;30;42m', '\x1b[1;30;41m', '']
    colored = ""
    for ch in range(len(word)):
        try:
            tone = int(tones[ch])
        except:
            tone = 0
        colored += colors[tone] + word[ch] + '\x1b[0m'
    return colored


def test_pinyin(question_num, color=True): # number of questions to do
    print("Enter pinyin (without tone markings) for the following:")
    words, weights = weighted_wordlist(pinyin_data) ###
    for i in range(question_num):
        word = np.random.choice(words, p=weights, replace=False)
        if color:
            word_c = colorize(word, entries[word][1])
            pinyin = input(str(i+1) + ") " + word_c+" : ")
        else:
            pinyin = input(str(i+1) + ") " + word+" : ")
        pinyin = [ch.lower() for ch in pinyin if ch.isalpha()]
        pinyin = "".join(pinyin)
        correct = entries[word][0] ###
        correct = [ch.lower() for ch in correct if ch.isalpha()]
        correct = "".join(correct)
        if pinyin == correct:
            print("Correct!")
            pinyin_data[word][0] += 1 ###
        else:
            print("Incorect.", entries[word][0]) ###
            pinyin_data[word][0] -= 1 ###
        pinyin_data[word][1] = int(time.time()) ###
        print("\n")
        
        
def test_english(question_num, color=True): # number of questions to do
    print("Enter English translations for the following:")
    words, weights = weighted_wordlist(english_data) ###
    for i in range(question_num):
        word = np.random.choice(words, p=weights, replace=False)
        if color:
            word_c = colorize(word, entries[word][1])
            pinyin = input(str(i+1) + ") " + word_c+" : ")
        else:
            pinyin = input(str(i+1) + ") " + word+" : ")
        pinyin = [ch.lower() for ch in pinyin if ch.isalpha()]
        pinyin = "".join(pinyin)
        correct = entries[word][2] ###t
        correct = [ch.lower() for ch in correct if ch.isalpha()]
        correct = "".join(correct)
        if pinyin == correct:
            print("Correct!")
            english_data[word][0] += 1 ###
        else:
            print("Incorect:", entries[word][2]) ###
            english_data[word][0] -= 1 ###
        english_data[word][1] = int(time.time()) ###
        print("\n")
        

def update_results(results_file):
    # Currently does naive implementation, rewriting everything even if unchanged
    with open(results_file, "w") as f:
        header = "*HANZI\tHANZI_SCORE\tTIMESTAMP\tPINYIN_SCORE\tTIMESTAMP\tTONE_SCORE\tTIMESTAMP\tENGLISH_SCORE\tTIMESTAMP*\n"
        f.write(header)
        for word in entries:
            hanzi = "\t" + str(hanzi_data[word][0]) + "\t" + str(hanzi_data[word][1])
            pinyin = "\t" + str(pinyin_data[word][0]) + "\t" + str(pinyin_data[word][1])
            tone = "\t" + str(tone_data[word][0]) + "\t" + str(tone_data[word][1])
            english = "\t" + str(english_data[word][0]) + "\t" + str(english_data[word][1])
            line = word + hanzi + pinyin + tone + english + "\n"
            f.write(line)
    print("Results updated.")
        
        

# After tunning tests, to save results:
# update_results(results_file)

if __name__ == "__main__":
    wordlist_file = "data/wordlist.txt"
    results_file = "data/results.txt"
    # entries serves as a general dictionary
    # the others serve to record timestamps of testing and test results, for calculating repetition weights
    entries, hanzi_data, pinyin_data, tone_data, english_data = initialize(wordlist_file, results_file)
    continue_flag = True
    while continue_flag:
        test_type = input("Which test: (T)ones, (P)inyin, or (E)nglish? ")
        try:
            test_type = test_type.lower()[0]
        except:
            print("Invalid entry. Please write 'Tones', 'Pinyin', or 'English'")
        test_num = input("How many questions do you want to do? Please enter a number : ")
        test_num = int(test_num)
        if test_type == "t":
            test_tones(test_num)
        elif test_type == "p":
            test_pinyin(test_num)
        elif test_type == "e":
            test_english(test_num)
        response = input("Test completed. Continue? (yes/no): ")
        response = response.lower()[0]
        if response == "n":
            continue_flag = False
    update_results(results_file)