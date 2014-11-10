from __future__ import division
import snap

# default considers out degree
def getDegDist(graph, inDeg=False):
	numNodes = graph.GetNodes()
	degToCntV = snap.TIntPrV()
	if inDeg:
		histo = snap.GetInDegCnt(graph, degToCntV)
		degDist = open('degdistIn.tab', 'w')
	else:
		histo = snap.GetOutDegCnt(graph, degToCntV)
		degDist = open('degdistOut.tab', 'w')
	total = 0
	freq = 0
	prevDeg = 0
	foundMedian = False
	deg = "in degree" if inDeg else "out degree"
	for i in degToCntV:
		degDist.write("%d\t%f\n" % (i.GetVal1(), i.GetVal2()))
		total += i.GetVal1()*i.GetVal2()
		freq += i.GetVal2()
		if freq > numNodes / 2 and not foundMedian:
			foundMedian = True
			if prevDeg == 0:
				print "median %s: %f" % (deg, i.GetVal1())
			else:
				print "median %s: %f" % (deg, (prevDeg + i.GetVal1()) / 2)
		elif freq == numNodes / 2:
			prevDeg = i.GetVal1()
	print "average %s: %f" % (deg, (total/numNodes))

graph = snap.LoadEdgeList(snap.PNEANet, "edges.txt", 1, 2, ',')
print snap.GetClustCf(graph, -1)
	
getDegDist(graph)
getDegDist(graph, True)

components = snap.TCnComV()
snap.GetSccs(graph, components)
print "%d sccs" % components.Len()
mxScc = snap.GetMxScc(graph)
print "%d nodes in max scc" % mxScc.GetNodes()
diameter = snap.GetBfsFullDiam(mxScc, 100, True)
print diameter