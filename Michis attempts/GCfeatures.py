from urllib.request import urlopen
import json, base64, string, operator
####
#
# Simple approach to gain filtered and therefore useful wordlists/clouds out of text files such as readme.md
#
###
filter = base64.b64encode(b'id<20')
url = 'http://classifier.leimstaedtner.it/ajax.php?key=api:all&filter='+filter.decode("utf-8")
print(url)
response = urlopen(url)
data = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))

classes = ["DEV", "HW","EDU", "DOCS","WEB","DATA","OTHER","SKIP"]
wordlist = {}
for c in classes:
    wordlist[c] = {}

for sample in data:
    readme = base64.b64decode(sample["readme"]).decode("utf-8")
    #print(readme)
    readme_codefree = "";
    for no_code in readme.split("```")[::2]: # skip content code in e.g.  blalba```code```blabla
        readme_codefree += no_code
    #print(readme_codefree)
    for word in [word.strip(string.punctuation) for word in readme_codefree.split()]:
        # Split readme_codefree into words and count up
        if(len(word) > 0):
            if not word in wordlist[sample["class"]]:
                wordlist[sample["class"]][word] = 1
            else:
                wordlist[sample["class"]][word] += 1

print(sorted(wordlist["DEV"].items(), key=operator.itemgetter(1)))
