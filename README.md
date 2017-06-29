# Running the program:

To run the program, from the terminal, enter:

```python run_tests.py```

Currently, the tone test only shows the Hanzi. To display the Pinyin instead, manually edit this script so the parameter ```question_format="py"``` in the function ```test_tones```.


# Adding new word to the wordlist:

From the terminal, run the script:

```python add_words.py```

This script allows you to search through a Chinese dictionary by pinyin or character, displaying all options when there are multiple matches. If you select an option to add to the wordlist, it automatically looks up and saves the hanzi, pinyin, tone, and english meaning to the wordlist. Optionally, you can edit the english definition to something that suits you better.

The wordlist is stored as chinese.txt in the following format:

```<HANZI>\t<PINYIN WITHOUT TONES>\t<TONES AS NUMBERS>\t<ENGLISH GLOSS>\n```

with a single tab between each item. However, there can be spaces within a single item, such as “I am” for 我是. The script lowercases everything anyways, so capitalization does not  matter. So you can also manually add entries to this document if you do not want to use the add_words script.

***

The results.txt file stores the results (a score for wrong/right guesses) and a timestamp when the last test was performed for a given word for a given category. These are used to calculate the frequency of a word coming up again in the tests. This is accessed and updated automatically (both when new words are added to the wordlist and when there are new scores/timestamps from performing tests), so it does not need to be manually edited.
