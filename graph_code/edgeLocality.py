from __future__ import division
import snap

graph = snap.PNEANet.New()
file = open('edges_sorted.txt', 'r')
hopsFreq = {}
hopsTotal = {}
degToCntV = snap.TIntPrV()
for line in file:
    arr = line.split(',')
    src = int(arr[1])
    dst = int(arr[2])
    if not graph.IsNode(src):
        graph.AddNode(src)
    if not graph.IsNode(dst):
        graph.AddNode(dst)
    dist = snap.GetShortPath(graph, src, dst, True)
    if dist in hopsFreq:
        hopsFreq[dist] += 1
    elif dist != -1:
        hopsFreq[dist] = 1
    distH = snap.TIntH()
    snap.GetShortPath(graph, src, distH, True)
    total = 0
    for node in distH:
        if distH[node] in hopsTotal:
            hopsTotal[distH[node]] += 1
        else:
            hopsTotal[distH[node]] = 1
    graph.AddEdge(src, dst)
file.close()
file2 = open('shortData.tab', 'w')
for inDeg in hopsFreq:
    if hopsFreq[inDeg]/hopsTotal[inDeg] == 1:
        print inDeg
    file2.write("%d\t%f\n" % (inDeg, hopsFreq[inDeg]))
file2.close()