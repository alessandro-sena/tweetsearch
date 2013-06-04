from collections import defaultdict
from nltk import wordpunct_tokenize

import re
import sys
sys.path.insert(0, "Python-Language-Detector")
import languageIdentifier
languageIdentifier.load('Python-Language-Detector/trigrams/')

# Twitter Related Functions

def filter_tweet(tweet, langs=['en']):
    try:
        # Extracts urls
        urls = re.findall('http[s]?:\\\/\\\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet['text'] )
        text = tweet['text'].encode('utf-8')

        # Accepts Only:
        #   English Tweets
        #   Without urls
        #   No RTs
        #   No Replies 
        if (
            languageIdentifier.identify(text, 300, 300) in langs 
            and "retweeted_status" not in tweet 
            and len(urls) < 1 
            and 'http' not in tweet['text'].lower() # Need to fix this latter >.<
            and not 'rt' == text[:2].lower() 
            and not '@' in tweet['text'].lower() # No Replies or mentions for a while ;D
        ): 
            return True
        else:
            return False
    except Exception, error:
        #print error
        return False

def tokenize_tweet(text):
    # Extracts urls
    #urls = re.findall('http[s]?:\\\/\\\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)#re.findall('http', text)
    #if len(urls) >= 0:
    #    print text
    # Normalizes text and aplies simple tokenization
    text = wordpunct_tokenize(text.lower())

    # Fix the mentions and hashtags
    t = []
    i =0 
    if text[-1] in ['@', '#']:
       text.append('')
    while i < len(text):
        if text[i] not in ['@', '#']:
            t.append(text[i])
        else:
            t.append(text[i]+text[i+1])
            i+=1
        i+=1
    text = t   

    return text
