from collections import defaultdict
import cjson
import os 
import math
import utils
import re


class TweetSearch():

    def __init__(self):
        # Inverted list index
        self.index = defaultdict(list)

        # Document frequency of each word
        self.df = defaultdict(int)

        # Number of Tweets in the index
        self.N = 0

        # IDF of each word
        self.idf = defaultdict(float)

        # Norm of each tweet
        self.norms = defaultdict(float)

    def index_collection(self, collection_dir, base_limit=10**7):
        stop = False
        i = 0
        cwd = os.getcwd()
        os.chdir(collection_dir)
        for f in os.listdir("."):
            print f
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
                    continue
                print line.strip()


                if i > base_limit:
                    stop = True
                    break
            fin.close()
        os.chdir(cwd)

        # Update the idf and norms
        self.update_idf()
        self.update_norms()
        print "indexed"

    def index_tweet(self, tweet):
        print tweet
        tid = tweet['id']
        text = tweet['text']
        counter = defaultdict(int)

        #tokens = utils.tokenize_tweet(text)
        # Extract only the words as tokens
        tokens = re.compile('\w+').findall(text.lower()) 


        for token in tokens:
            counter[token] += 1

        for word, freq in counter.iteritems():
            tf = 1.0 + math.log(freq, 2)
            self.index[word].append((tid, tf))
            self.df[word] += 1

        self.N += 1

    def update_idf(self):
        N = float(self.N)
        for word, df in self.df.iteritems():
            self.idf[word] = math.log((N/float(df)), 2)

    def update_norms(self):
        # Cleans the norm vector 
        # This needs to be done, cause the idf's change 
        norms = defaultdict(float)

        for word, inverted_list in self.index.iteritems():
            for tid, tf in inverted_list:
                norms[tid] += (tf*self.idf[word])**2

        for tid, norm in norms.iteritems():
            norms[tid] = math.sqrt(norm)

        self.norms = norms        

    def search(self, query):

        accumulator = defaultdict(float)
        counter = defaultdict(int)

        # Extract only the words as tokens
        tokens = re.compile('\w+').findall(query.lower()) 
        #tokens = utils.tokenize_tweet(query)
        
        for token in tokens:
            counter[token] += 1

        # Calculates the query norm
        query_norm = 0.0 
        for word, freq in counter.iteritems():
            print "%s - %f" % (word, self.idf[word])
            tf = freq # 1+math.log(freq, 2)            
            query_norm += (tf*self.idf[word])**2
            counter[word] = tf
        query_norm = math.sqrt(query_norm)
        print query_norm

        for word, qtf in counter.iteritems():
            for tid, dtf in self.index[word]:
                accumulator[tid] += (self.idf[word]**2)*qtf*dtf

        scores = [ (tid, value/(query_norm*self.norms[tid])) for tid, value in accumulator.iteritems()] 

        scores = sorted(scores, key=lambda tup: tup[1])[::-1]

        return scores

def test():
    ts = TweetSearch()
    ts.index_collection('test_collection')
    print ts.N

    print '--------------------'
    for item in ts.idf.iteritems():
        print "%s: %f" % item

    print '--------------------'
    for item in ts.norms.iteritems():
        print "%s: %f" % item

    print ts.search("to do")

def main():
    ts = TweetSearch()
    ts.index_collection('stream')

    print ts.search('so excited for the last few eps of this season!!! ahhh')[:10]

if __name__ == "__main__":
    test()    

                                
