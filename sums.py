# For testing results
import os
import sys

def sumWeightsTargetVals(tvfname):
    total = 0
    with open(tvfname) as tvf:
        for line in tvf:
            src, dst, weight = line.split(' ')
            total += float(weight)
    return total

def sumWeightsNetwork(networkfname):
    with open(networkfname) as networkf:
        processEdge = False
        total = 0
        for line in networkf:
            if processEdge:
                src, dst, weight = line.split(' ')
                total += float(weight)
            elif line.find('*Edges ') == 0:
                    processEdge = True
        return total

if __name__ == '__main__':
    total = 0
    for filename in os.listdir(sys.argv[1]):
        if filename.startswith('.'):
            continue
        subt = sumWeightsTargetVals(sys.argv[1] + filename + '/TargetVals.txt')
        print subt
        total += subt
    print 'Final total is %d' % total
    # print 'Network total is %g' % sumWeightsNetwork(prefix + '/network.txt')
    #print 'Target edge total is %g' % sumWeightsTargetVals(prefix + '/TargetVals.txt')