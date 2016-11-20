import base64
from urllib2 import Request, urlopen, URLError
import json

#hier drinnen muss sehr viel noch komplett überarbeitet werden

# Constants
max_stars = 60000 # Max found in data was 52762
max_forks =  10000 # Max found in data was 9287
max_watches = 4000 # Max found in data was 3709

#muss lesbarer gemacht werden
def api_call(equal=False):
    """Standard request to the database"""
    filter = base64.b64encode(b'id>0')
    url = None
    if equal:
        url = 'http://classifier.leimstaedtner.it/ajax.php?key=api:equal&filter='+filter.decode("utf-8")
    else:
        url = 'http://classifier.leimstaedtner.it/ajax.php?key=api:all&filter='+filter.decode("utf-8")
    request = Request(url)
    try:
        response = urlopen(request)
        data = json.load(response)
    except URLError, e:
        print 'Error with api call', e
    return data

def get_unlabeled_data(whatIWant='description'):
    """Hole data als dict"""
    #data = api_call(url="Gimme unlabeld pls")
    
    features = []

    for i in xrange(len(data)):
        feature = None
        if whatIWant == 'readme':
            #nur die readme ist anscheinend decoded
            feature = text_from_base64(data[i][whatIWant]).decode('utf-8')
        elif whatIWant == 'meta':
            """ 
            Availible metadata: description, author, url, tree, watches, 
                                class, languages, tagger, stars, readme, 
                                forks, id, name
            """
            feature = []
            sample = data[i]
            feature.append(float(sample['watches']) / max_watches)
            feature.append(float(sample['stars']) / max_stars)
            feature.append(float(sample['forks']) / max_forks)
            features.append(feature)
        else:
            feature = data[i][whatIWant]
        if whatIWant != 'meta':
           # feature = process_text(feature)
        features.append(feature)
    return features
    
def text_from_base64(text):
    """Convert text back from base64"""
    missing_padding = len(text) % 4
    if missing_padding != 0:
        text += b'='* (4 - missing_padding)
    text = None
    try:
        text = base64.b64decode(text)
    except TypeError:
        print "Error decoding readme"
    return text

