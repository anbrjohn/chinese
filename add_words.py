# https://www.mdbg.net/chinese/dictionary?page=cedict

with open("data/cedict_ts.u8") as f:
    char_dic = {}
    pinyin_dic = {}
    for line in f:
        if line[0] != "#":
            line = line.split("/")
            meaning = line[1:-1]
            meaning = ". ".join(meaning)
            info = line[0].split(" ")
            traditional = info[0]
            simplified = info[1]
            reading = " ".join(info[2:])       
            pinyin = "".join([ch.lower() for ch in reading if ch.isalpha()])
            tones = "".join([ch for ch in reading if ch.isdigit()])
            #meaning = " ".join(line[3:]).strip()
            if simplified not in char_dic:
                char_dic[simplified] = [[traditional, pinyin, tones, meaning]]
            else:
                char_dic[simplified] += [[traditional, pinyin, tones, meaning]]
            if pinyin not in pinyin_dic:
                pinyin_dic[pinyin] = [[simplified, traditional, tones, meaning]]
            else:
                pinyin_dic[pinyin] += [[simplified, traditional, tones, meaning]]
                

def search_by_pinyin(word):
    word = "".join([ch.lower() for ch in word if ch.isalpha()])
    if word in pinyin_dic:
        options = pinyin_dic[word]
        if len(options) == 1:
            print("1 entry found:")
        else:
            print(len(options), "entries found:")
        print("\tSimplified\tTraditional\tTones\tMeaning")
        i = 1
        for entry in options:
            if entry[0] == entry[1]:
                traditional = "  "
            else:
                traditional = entry[1]
            print(i, ")\t", entry[0], "\t\t", traditional, "\t\t", entry[2], "\t", entry[3])
            i += 1
    else:
        #print("Word not found in pinyin dictionary.")
        options = []
    return options


def search_by_char(word):
    word = "".join([ch.lower() for ch in word if ch.isalpha()])
    if word in char_dic:
        options = char_dic[word]
        if len(options) == 1:
            print("1 entry found:")
        else:
            print(len(options), "entries found:\n")
        print("\tTraditional\tPinyin\t\tTones\tMeaning")
        i = 1
        for entry in options:
            if word == entry[0]:
                traditional = "  "
            else:
                traditional = entry[0]
            print(i, ")\t", traditional, "\t\t", entry[1], "\t\t", entry[2], "\t", entry[3])
            i += 1
    else:
        #print("Word not found in hanzi dictionary.")
        options = []
    return options


    
def edit_entry(entry, word, word_type):
    edit_meaning = input("Edit meaning (press enter to copy as is): ")
    if len(edit_meaning) == 0:
        meaning = entry[3]
    else:
        meaning = edit_meaning
    with open("data/wordlist.txt", "a") as f:
        if word_type == "py":
            pinyin = word
            char = entry[0]
        else:
            char = word
            pinyin = entry[1]
        tones = str(entry[2])
        line = "\n" + char + "\t" + pinyin + "\t" + tones + "\t" + meaning
        f.write(line)
    print("Saved to wordlist.")
    


def add_to_list():
    word = 1
    while word != "0":
        word = input("Enter desired word (as hanzi or pinyin) (0 to exit): ")
        word = [ch.lower() for ch in word if ch.isalpha()]
        word = "".join(word)
        char_options = search_by_char(word)
        pinyin_options = search_by_pinyin(word)
        if len(char_options) == 0 and len(pinyin_options) == 0:
            print("No words found in dictionary.")
            return
        elif len(pinyin_options) > 0:
            word_type = "py"
            options = pinyin_options
        else:
            word_type = "hz"
            options = char_options
        if len(options) == 1:
            selection = input("Select word (y/n)? : ")
            selection = selection.lower()[0]
            if str(selection) == "1":
                selection = "y"
            elif str(selection) == "0":
                selection = "n"
            elif str(selection) == "2":
                selection = "n"
            if selection == "y":
                edit_entry(options[0], word, word_type)
            else:
                return
        else:
            selection = input("Select word number (0 to exit) : ")
            if str(selection) == "0":
                return
            selection = int(selection)
            edit_entry(options[selection - 1], word, word_type)

            
if __name__ == "__main__":
    add_to_list()