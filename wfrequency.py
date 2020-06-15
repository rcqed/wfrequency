import re
import string
import sys,os

os.chdir(sys.path[0])

f = open("./words.txt","w")
r = open(sys.argv[1], 'r')
strs =r.read()

s = re.findall("\w+",str.lower(strs))
l = sorted(list(set(s)))

for i in l:
    m = re.search("\d+",i)
    n = re.search("\W+",i)
    if not m and  not n and len(i)>4:
        f.write(i +" : "+str(s.count(i))+"\n")

r.close()
f.close()