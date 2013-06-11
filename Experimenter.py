import sys

import cjson

import JaccardSearch as JS
import TweetSearch as TS

bases = [10** x for x in xrange(3,8)]
tweets = []
folds = []


# Load the tweets
fin = open(sys.argv[1])
for line in fin:	
	d = cjson.decode(line)
	tweets.append(
		(
			d['id'],
			d['text'],
		)
	)
fin.close()

for base in bases: 
	filtered = [(tid, text) for tid, text in tweets if tid.find("b%dt" % base)]

	js = JS.JaccardSearch()
	js.index_collection(sys.argv[2], base_limit=base)

	ts = TS.TweetSearch()
	ts.index_collection(sys.argv[2], base_limit=base)

	for tid, tweet in filtered:
		# Takes only the top tweet score 
		j = js.search(tweet)[0][1]
		c = ts.search(tweet)[0][1]

		t = (tid, tweet, j, c)
		print t
		break

	del(ts)
	del(js)