from __future__ import division
import math

degf = open('degdistOut.tab', 'r')

def writeratiofrequency(distribution, name, xmin):
	f = open(name, 'w')
	total = 0
	for i in distribution:
		if i >= xmin:
			total += distribution[i]
	for i in distribution:
		if i >= xmin:
			f.write("%d,%f\n" % (i, distribution[i]/total))

# writefile(dist(freq(mobyf)), "mobydistf.tab")
# writefile(dist(freq(donf)), "dondistf.tab")

def computealpha(rawdistribution, xmin):
	alpha = 0
	count = 0
	for i in rawdistribution:
		if i >= xmin:
			alpha += rawdistribution[i]*math.log(i/xmin)
			count += rawdistribution[i]
	if alpha == 0:
		return 0
	alpha = 1+count*(1/alpha)
	return alpha

def plotxmin(rawdistribution, name):
	xminf = open(name, 'w')
	for i in range(1, 10000):
		xminf.write("%d,%f\n" % (i, computealpha(rawdistribution, i)))
	
# after finding xmin
#writefile(mobydist, "mobydistf.tab")
#writefile(mobydist, "dondistf.tab")
#plot [1:1000] ((2.01437-1)/10)*((x/10)**(-2.01437)), "mobydistf.tab"
#plot [1:1000] ((1.877095-1)/10)*((x/10)**(-1.877095)), "dondistf.tab"

degfreq = {}
for line in degf:
	tokens = line.split(',')
	degfreq[int(tokens[0])] = int(float(tokens[1]))

writeratiofrequency(degfreq, "outdegFrequency.csv", 7)
print "alpha for out degree distribution is %f" % computealpha(degfreq, 7) # 7 observed from log-log plot of out degree distribution
# alpha = 2.100595

numnodes = sum([degfreq[i] for i in degfreq])
degratio = {}
for i in degfreq:
    degratio[i] = degfreq[i]/numnodes
q = {} # excess degree dist
total = sum([degfreq[i] for i in degfreq])
for deg in degfreq:
    if deg >= 1:
        q[deg-1] = degfreq[deg]/total
qavg = sum([q[i]*i for i in q]) / sum([q[i] for i in q])
qvar = sum(q[i]*(qavg - i)**2 for i in q) / sum([q[i] for i in q])
total = 0
for i in q:
    for j in q:
        if i not in degratio or j not in degratio:
            continue
        total += i*j*(degratio[i]*degratio[j]-q[i]*q[j])
print total/qvar
