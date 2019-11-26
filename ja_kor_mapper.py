#!/usr/bin/env python3
import csv
import string


nouns_file = "kor-jap-nouns.csv"

"""

This script generates a mapping between japanese kanji -> korean characters
and korean -> kanji characters.


"""


hiragana_strings = ''.join([chr(i) for i in range(0x3040, 0x30a0)])
katakana_strings = ''.join([chr(i) for i in range(0x30a0, 0x3100)])

hiragana_set = set(hiragana_strings)
katakana_set = set(katakana_strings)

letters = string.ascii_letters
letters_set= set(letters)


def check_has_kanji(jap_word):
    word_chars = set(jap_word)
    # check if word_chars has any characters not in the set of 
    # - hiragana, katakana and letters.

    word_chars -= hiragana_set
    word_chars -= katakana_set
    word_chars -= letters_set
    return len(word_chars) > 0


# nouns file parsing 
jap_kor_tuples = []
skip_n_headers = 2
with open(nouns_file, newline='') as f:
    reader = csv.reader(f)
    i = 0
    for row in reader:
        if i < skip_n_headers:
            i+=1
            continue
        kor = row[1]
        jap = row[4] 
        if jap == '' or not check_has_kanji(jap):
            continue
        jap_kor_tuples.append((jap, kor))
        print("korean: {}, japanese: {}".format(kor,jap))

print("len kanji stuff: {}".format(len(jap_kor_tuples)))

jap_kor_map = {} # maps a kanji character to a set of korean characters.
kor_jap_map = {} # maps a korean character to a set of japanese kanji characters.

def insert_to_map(x,y, mapping):
    if mapping.get(x) is None:
        mapping[x] = set([y])
    else:
        mapping[x].update(y)


for tup in jap_kor_tuples:
    jap, kor = tup

    # go by min len.
    l = min(len(jap), len(kor))
    for i in range(l):
        if check_has_kanji(jap[i]):
            insert_to_map(jap[i],kor[i], jap_kor_map)
            insert_to_map(kor[i], jap[i], kor_jap_map)


print("map:")
#print(jap_kor_map)
print(kor_jap_map)




