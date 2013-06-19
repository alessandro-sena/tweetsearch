import sys
import re

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

import cjson

results = []
fin = open(sys.argv[1])
for line in fin:
    tid, j, c = line.split(',') 
    j, c = float(j), float(c)
    results.append((tid, j, c))
fin.close()  


# All the baselines
# patterns = ["hi\d+b%d" % 10**x for x in xrange(3,7)]
for base in xrange(3, 7):
    b = 10 ** base
    for top in [10, 25, 50, 100]:
        patterns = ["hi\d+b%d" % b]

        for order in [2,3,4,5]:
            patterns += ["so%db%dt%d" % (order, b, top)] 

        #print patterns
        #continue

        # Just changing order, size and top fixed 

        fig = plt.figure()

        xs = np.linspace(0,1,200)
        for p in patterns:

            regex = re.compile(p)
            if sys.argv[2] == 'c': 
                data = [c for tid, j, c in results if regex.search(tid)]
            else:
                data = [j for tid, j, c in results if regex.search(tid)]

            density = gaussian_kde(data)
            density.covariance_factor = lambda : .25
            density._compute_covariance()
            plt.plot(xs,density(xs), label=p)

        if sys.argv[2] == 'c': 
            plt.xlabel('Cosine')
        else:
            plt.xlabel('Jaccard')

        plt.ylabel('Density')
        plt.legend()
        print ''' 
\\begin{figure}[!htb]
    \centering
    \includegraphics[scale=.40]{similaridades/b%dt%d%s.png}
    \caption{b%dt%d%s}
    \label{Baseline Jaccard}
\end{figure}
        ''' % (b, top, sys.argv[2], b, top, sys.argv[2])

        plt.savefig("b%dt%d%s.png" % (b, top, sys.argv[2]))
        plt.cla()
        plt.plot()
        fig.clear()



