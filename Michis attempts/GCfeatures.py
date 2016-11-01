# -*- coding: utf-8 -*-
from urllib.request import urlopen
from subprocess import call
import json, base64, string, operator, math, copy
import sys, io

#### PYTHON 3 ONLY
# 
# Simple approach to gain filtered and therefore useful wordlists/clouds out of text files such as readme.md
#
# Basic idea: create dictionaries with wordcounts per class. Sort out words with <= 1 count and words with high cross-class correlation
# Each sample can then be hashed as a percentual word distribution of the entire wordlist
###
# Set output to utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), 'utf-8', 'strict')
def sort_words(wlist):
    # sorts the dictionary, BUT returns an array of tuples [(word, max-count),..-]
    for c in classes:
        wlist[c] = sorted(wlist[c].items(), key=operator.itemgetter(1), reverse=True)
    return wlist

def filter_top_words(wlist):
    # get only the top 10% of the values
    top_words = {}
    #print(wlist)
    sorted_words = sort_words(copy.deepcopy(wlist))
    #print(sorted_words)
    for c in classes:
        top_words[c] = dict(sorted_words[c][:max(0, math.floor(len(wordlist[c]) / 10))])
    #print(top_words)
    return top_words

filter = base64.b64encode(b'id>0')
url = 'http://classifier.leimstaedtner.it/ajax.php?key=api:all&filter='+filter.decode("utf-8")
print(url)
response = urlopen(url)
data = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
classes = ["DEV", "HW", "EDU", "DOCS", "WEB", "DATA", "OTHER", "SKIP"]
wordlist = {}
for c in classes:
    wordlist[c] = {}

for sample in data:
    # Adds words to the class specific list
    readme = base64.b64decode(sample["readme"]).decode("utf-8")
    #print(readme)
    readme_codefree = ""
    for no_code in readme.split("```")[::2]:
        # skip content code in e.g.  blalba```code```blabla
        readme_codefree += no_code
    #print(readme_codefree)
    for word in [elem.strip(string.punctuation) for elem in readme_codefree.split()]:
        # Split readme_codefree into words and count up
        if(len(word) > 0):
            if not word.lower() in wordlist[sample["class"]]:
                wordlist[sample["class"]][word.lower()] = 1
            else:
                wordlist[sample["class"]][word.lower()] += 1

for c in classes:
    # Remove words with <= 1 count
    wordlist[c] = {k: v for k, v in wordlist[c].items() if v > 1}

#wordlist = sort_words(wordlist)
top_words = filter_top_words(wordlist)
merged_top_words = []
to_be_removed = []

for c in classes:
    # Check top 10% of words if present in other word-clouds as well
    for w in top_words[c]:
        merged_top_words.append(w)
        class_count = 1
        for ctemp in classes:
            if ctemp != c:
                for wtemp in top_words[ctemp]:
                    # Wow, a quadruple loop. Should definitely be improved!
                    if wtemp == w:
                        class_count += 1
                if class_count > len(classes) * 1 / 4: 
                    # At least 2 different classes should have many occurences of this word
                    to_be_removed.append(w)
                    break

for c in classes:
    # Remove words from the to_be_removed list
    wordlist[c] = {k: v for k, v in wordlist[c].items() if k not in to_be_removed}
print(to_be_removed)
print([w for w in merged_top_words if w not in to_be_removed])

print(wordlist)