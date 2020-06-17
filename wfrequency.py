# -*- coding: utf-8 -*-

import pandas as pd
import re
import string
import sys,os

os.chdir(sys.path[0])  #指定目录

#读取字典，并取word，translation这两列
df_dict = pd.read_csv("./stardict.csv",low_memory=False)
df_dict = df_dict[["word","translation"]]

#读取认识的单词，取word列
df_known = pd.read_excel("known.xlsx")
df_known = df_known[["word"]]

#打开要处理的文章
reader = open(sys.argv[1], 'r')
strs =reader.read()

#使用正则表达式，把单词提取出来，并都修改为小写格式
strs_q = re.findall("\w+",str.lower(strs))
#去除列表中的重复项，并排序
word_list = sorted(list(set(strs_q)))

#去除含有数字和符号，以及长度小于2的字符串
new_words = []
word_count = []
for i in word_list:
    m = re.search("\d+",i)
    n = re.search("\W+",i)
    if not m and  not n and len(i)>2:
        new_words.append(i)  #获取单词转为list列表
        word_count.append(strs_q.count(i))  #获取词频并转为list列表
#将list列表整理为dataframe表格格式
df_words = pd.DataFrame({"word": new_words,"count":word_count})

#对比文章中提取的单词，并与字典的中文意思匹配
df_merge = pd.merge(
    left = df_dict,
    right = df_words,
    left_on = "word",
    right_on = "word"
)

#把dataframe表格转化为list列表
known_list=df_known["word"].tolist()

#从提取的单词中减去认识的单词
df_new=df_merge[~df_merge["word"].isin(known_list)]

#将表格输出到excle文件
df_new.to_excel("./words.xlsx")

#文章识别率计算
rate=df_new.shape[0]/df_merge.shape[0]
print("文章识别率：","%.2f%%" % (rate*100))

#文章难度判定
if rate > 0.95:
    print("难度：偏易")
elif rate < 0.75:
    print("难度：偏难")
else:
    print("难度：适中")

input("回车关闭窗口")