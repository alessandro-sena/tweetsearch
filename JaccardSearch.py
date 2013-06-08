from collections import defaultdict
import cjson
import os 
import math
import utils


class JaccardSearch():

    def __init__(self):


        # Stores the trigrams of the tweets
        self.tweets = {}

        # Number of Tweets in the index
        self.N = 0

    
    def index_collection(self, collection_dir, base_limit=10**7):
        stop = False
        i = 0
        cwd = os.getcwd()
        os.chdir(collection_dir)
        for f in os.listdir("."):
            if stop:
                break
            fin = open(f)
            for line in fin:
                try:
                    tweet = cjson.decode(line)
                except Exception, error:
                    print error
                    continue

                try:
                    if utils.filter_tweet(tweet):
                        self.index_tweet(tweet)
                        i += 1
                except Exception, error:
                    print error

                if i >= base_limit:
                    stop = True
                    break
            fin.close()
        os.chdir(cwd)

        print "indexed"


    def index_tweet(self, tweet):
        tid = tweet['id']
        text = tweet['text']
        trigrams = utils.get_trigrams(text)
        self.tweets[tid] = trigrams
        self.N += 1
  

    def search(self, text):
        qtrigrams = utils.get_trigrams(text)
        scores = []  
        for tid, dtrigrams in self.tweets.iteritems():
            union = len(qtrigrams | dtrigrams)
            intersection = len(qtrigrams & dtrigrams)
            scores.append((tid, intersection/float(union)))
        #print scores

        
        scores = sorted(scores, key=lambda tup: tup[1])[::-1]

        return scores

def test():
    js = JaccardSearch()
    #ts.index_collection('stream')
    js.index_tweet({'id': 1, 'text': "a b c To do is to be To be is to do"})
    js.index_tweet({'id': 2, 'text': "a b c To be or not to be I am what I"})
    js.index_tweet({'id': 3, 'text': "a b c I think therefore I am Do be do be do"})
    js.index_tweet({'id': 4, 'text': "a b c Do do do da da da Let it be Let"})
    
    print js.search("a b c to")

def main():
    js = JaccardSearch()
    js.index_collection('stream')
    print js.search('so excited for the last few eps of this season!!! ahhh')[:10]
    print js.N

if __name__ == "__main__":
    main()    

                                
