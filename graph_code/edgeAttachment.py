from __future__ import division
import snap

graph = snap.PNEANet.New()
file = open('edges_sorted.txt', 'r')
inDegFreq = {}
inDegTotal = {}
degToCntV = snap.TIntPrV()
for line in file:
    arr = line.split(',')
    src = int(arr[1])
    dst = int(arr[2])
    if not graph.IsNode(src):
        graph.AddNode(src)
    if not graph.IsNode(dst):
        graph.AddNode(dst)
    inDeg = graph.GetNI(dst).GetInDeg()
    if inDeg in inDegFreq:
        inDegFreq[inDeg] += 1
    else:
        inDegFreq[inDeg] = 1
    snap.GetInDegCnt(graph, degToCntV)
    for pair in degToCntV:
        deg = pair.GetVal1()
        fr = pair.GetVal2()
        if deg in inDegTotal:
            inDegTotal[deg] += fr
        else:
            inDegTotal[deg] = fr
    graph.AddEdge(src, dst)
file.close()
file2 = open('edgeAttachmentData.tab', 'w')
total = 0
for inDeg in inDegFreq:
    total += inDegFreq[inDeg]
a = [0 for i in range(36)]
b = [0 for i in range(36)]
def intToMap(i):
	if i < 10:
		return i-1
	if i < 100:
		return int(i/10)+8
	if i < 1000:
		return int(i/100)+17
	if i < 10000:
		return int(i/1000)+26
def mapToInt(i):
	if i < 9:
		return i+1 
	if i < 18:
		return (i-8)*10
	if i < 27:
		return (i-17)*100
	if i < 36:
		return (i-26)*1000
for inDeg in inDegFreq:
	a[intToMap(inDeg)] += inDegFreq[inDeg]
	b[intToMap(inDeg)] += inDegTotal[inDeg]
for inDeg in range(len(a)):
	if b[inDeg] != 0:
		file2.write("%d\t%f\n" % (mapToInt(inDeg), a[inDeg]/b[inDeg]))
file2.close()