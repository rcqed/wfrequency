# -*- coding: utf-8 -*-

import pandas as pd
import re
import string
import sys,os

os.chdir(sys.path[0])

df_dict = pd.read_csv("./stardict.csv")
df_dict = df_dict[["word","translation"]]

reader = open(sys.argv[1], 'r')
strs =reader.read()

strs_q = re.findall("\w+",str.lower(strs))
word_list = sorted(list(set(strs_q)))

new_words = []
word_count = []
for i in word_list:
    m = re.search("\d+",i)
    n = re.search("\W+",i)
    if not m and  not n and len(i)>4:
        new_words.append(i)
        word_count.append(strs_q.count(i))
df_words = pd.DataFrame({"word": new_words,"count":word_count})

df_merge = pd.merge(
    left = df_dict,
    right = df_words,
    left_on = "word",
    right_on = "word"
)

df_merge.to_excel("./words.xlsx")