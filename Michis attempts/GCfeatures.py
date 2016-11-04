# -*- coding: utf-8 -*-
from subprocess import call
import urllib2, json, base64, string, operator, math, copy, sys, io
from nltk.stem import PorterStemmer

#### PYTHON 3 ONLY
# Simple approach to gain filtered and therefore useful wordlists/clouds out of text files such as readme.md
#
# Basic idea: create dictionaries with wordcounts per class. Sort out words with <= 1 count and words with high cross-class correlation
# Each sample can then be hashed as a percentual word distribution of the entire wordlist
###
class PrettyWords:
    def __init__(self):
        print("PrettyWords module started")
        # Set output to utf-8
        if sys.version_info >= (3, 0):
            sys.stdout = io.TextIOWrapper(sys.stdout.detach(), 'utf-8', 'strict')

        self.classes = ["DEV", "HW", "EDU", "DOCS", "WEB", "DATA", "OTHER", "SKIP"]
        self.wordlist = {}
        for c in self.classes:
            self.wordlist[c] = {}

        self.data = self.getJson()
        self.generate_histogram()
        self.remove_loner()
        self.remove_overlaps()


    def getJson(self):
        print("Getting data from server")
        filter = base64.b64encode(b'id>0')
        url = 'http://classifier.leimstaedtner.it/ajax.php?key=api:all&filter='+filter.decode("utf-8")
        print(url)
        f = urllib2.urlopen(url)
        data = json.loads(f.read().decode('utf-8'))
        f.close()
        return data

    def sort_words(self, wlist):
        print("Sorting words")
        # sorts the dictionary, BUT returns an array of tuples [(word, max-count),..-]
        for c in self.classes:
            wlist[c] = sorted(wlist[c].iteritems(), key=operator.itemgetter(1), reverse=True)
        return wlist

    def filter_top_words(self, wlist):
        print("Top words are being chosen")
        # get only the top 10% of the values
        top_words = {}
        #print(wlist)
        sorted_words = self.sort_words(copy.deepcopy(wlist))
        #print(sorted_words)
        for c in self.classes:
            top_words[c] = dict(sorted_words[c][:max(0, int(math.floor(len(sorted_words[c]) / 10)))])
        #print(top_words)
        return top_words

    def generate_histogram(self):
        print("Generating histogram")

        # Create Stemmer to shorten every word
        # See https://de.wikipedia.org/wiki/Porter-Stemmer-Algorithmus
        stemmer = PorterStemmer()

        for sample in self.data:
            # Adds words to the class specific list
            readme = base64.b64decode(sample["readme"]).decode("utf-8")
            #print(readme)
            readme_codefree = ""
            for no_code in readme.split("```")[::2]:
                # skip content code in e.g.  blalba```code```blabla
                readme_codefree += no_code
            #print(readme_codefree)
            for word in [elem.strip(string.punctuation) for elem in readme_codefree.split()]:
                word = stemmer.stem(word)
                # Split readme_codefree into words and count up
                if(len(word) > 0):
                    if not word.lower() in self.wordlist[sample["class"]]:
                        self.wordlist[sample["class"]][word.lower()] = 1
                    else:
                        self.wordlist[sample["class"]][word.lower()] += 1
    def remove_loner(self):
        print("Removing single standing words")
        for c in self.classes:
            # Remove words with <= 1 count
            self.wordlist[c] = {k: v for k, v in self.wordlist[c].iteritems() if v > 1}

    def remove_overlaps(self):
        print("Removing overlapping words")
        #wordlist = sort_words(wordlist)
        top_words = self.filter_top_words(self.wordlist)
        merged_top_words = []
        to_be_removed = []

        for c in self.classes:
            # Check top 10% of words if present in other word-clouds as well
            for w in top_words[c]:
                merged_top_words.append(w)
                class_count = 1
                for ctemp in self.classes:
                    if ctemp != c:
                        for wtemp in top_words[ctemp]:
                            # Wow, a quadruple loop. Should definitely be improved!
                            if wtemp == w:
                                class_count += 1
                        if class_count > len(self.classes) * 1 / 4:
                            # At least 2 different classes should have many occurences of this word
                            to_be_removed.append(w)
                            break

        for c in self.classes:
            # Remove words from the to_be_removed list
            self.wordlist[c] = {k: v for k, v in self.wordlist[c].iteritems() if k not in to_be_removed}
        print("REMOVED words", to_be_removed)
        print("CLASS SPECIFIC words", [w for w in merged_top_words if w not in to_be_removed])
        print("FINAL wordlist", self.wordlist)

readmes = PrettyWords()
