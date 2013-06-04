from collections import defaultdict
import cjson
import os 
import math
import utils


class TweetSearch():

    def __init__(self):
        self.index = defaultdict(list)
        self.df = defaultdict(int)
        self.N = 0
        self.idf = defaultdict(float)
        self.norm = defaultdict(float)

    def index_collection(self, collection_dir):
        cwd = os.getcwd()
        os.chdir(collection_dir)
        for f in os.listdir("."):
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
                        break
                except Exception, error:
                    print error
            fin.close()
        os.chdir(cwd)

        self.update_idf()
        self.update_norms()


    def index_tweet(self, tweet):
        tid = tweet['id']
        text = tweet['text']
        #print text
        counter = defaultdict(int)

        tokens = utils.tokenize_tweet(text)
        #print tokens
        for token in tokens:
            counter[token] += 1
        #print counter

        for word, freq in counter.iteritems():
            freq = 1.0 + math.log(freq, 2)
            self.index[word].append((tid, freq))
            self.df[word] += 1

        self.N += 1

    def update_idf(self):
        N = float(self.N)
        for word, df in self.df.iteritems():
            self.idf[word] = math.log(1+(N/float(df)), 2)

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


    def search(self, query, ranking='vector'):

        accumulator = defaultdict(float)
        counter = defaultdict(int)
        tokens = utils.tokenize_tweet(query)

        for token in tokens:
            counter[token] += 1

        query_norm = math.sqrt(sum([(tf*self.idf[word])**2 for word, tf in counter.iteritems()]))
        print query_norm

        for word, qtf in counter.iteritems():
            for tid, dtf in self.index[word]:
                accumulator[tid] += (self.idf[word]**2)*qtf*dtf

        scores = [ (tid, value/query_norm*self.norms[tid]) for tid, value in accumulator.iteritems()] 

        sorted(scores, key=lambda tup: tup[1])[::-1]

        return scores



def main():
    ts = TweetSearch()
    #ts.index_collection('stream')
    ts.index_tweet({'id': 1, 'text': "To do is to be To be is to do"})
    ts.index_tweet({'id': 2, 'text': "To be or not to be I am what I am"})
    ts.index_tweet({'id': 3, 'text': "I think therefore I am Do be do be do"})
    ts.index_tweet({'id': 4, 'text': "Do do do da da da Let it be Let it be"})
    ts.update_idf()
    ts.update_norms()
    print ts.idf
    print ts.norms
    #print ts.search("Also Angelina Jolie can \"challenge\" society's views on the woman's body because her body already made her millions of dollars! #notsorry")

if __name__ == "__main__":
    main()    

                                
