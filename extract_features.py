from subprocess import Popen, call
import os
import collections

PREDICT_BIN_PATH = './LPmade/netlib/bin/predict'
# TODO originally 'PropFlow_5', 'IPageRank_D_0.85', 'JPageRank_D_0.85', 'RootedPageRank_D_0.15'
PREDICTORS = ['IDegree', 'JDegree', 'IVolume', 'JVolume', 'CommonNeighbor', 'JaccardCoefficient', 'AdamicAdar', 'PropFlow', 'IPageRank', 'JPageRank', 'RootedPageRank']

def make_if_needed():
    if not os.path.isfile(PREDICT_BIN_PATH):
        print('MAKING PREDICT BINARY, THIS WILL ONLY RUN THE FIRST TIME. WARNINGS EXPECTED')
        call('make', cwd = './LPmade/netlib/')

def genLabelFile(network_file_name, dirName):
    with open(network_file_name) as networkf:
        firstline = networkf.readline()
        prefix = '*Vertices '
        if firstline.find(prefix) != 0:
            print('ERROR first line of file was "{}"'.format(firstline))
            exit(1)
        numNodes = int(firstline[len(prefix):])
        processEdge = False
        weights = collections.Counter()
        intToExt = {}
        for line in networkf:
            if processEdge:
                src, dst, weight = line.split(' ')
                src = int(src)
                dst = int(dst)
                assert weights[(src, dst)] == 0
                weights[(src, dst)] = float(weight)
            else:
                if line.find('*Edges ') == 0:
                    processEdge = True
                else:
                    internal, external = map(int, line.split(' '))
                    intToExt[internal] = external
        if not processEdge:
            print('ERROR no edges found')
    with open(dirName + '/EdgeWeight.txt', 'w') as out:
        for src in xrange(numNodes):
            for dst in xrange(numNodes):
                out.write('{} {} {}\n'.format(intToExt[src], intToExt[dst], weights[(src, dst)]))#edges_weight_967791600_970383599

def write_features(network_file_name, dirName):
    if not os.path.isfile(network_file_name):
        print('Sorry, {} is not a valid file.'.format(network_file_name))
        return
    make_if_needed()
    parr = []; outarr = []
    for pred in PREDICTORS:
        out = open(dirName + '/' + pred + '.txt', 'w')
        parr.append(Popen([PREDICT_BIN_PATH, '-f', network_file_name, pred], stdout=out))
        outarr.append(out)
    genLabelFile(network_file_name, dirName)
    for p in parr:
        p.wait()
    for out in outarr:
        out.close()

if __name__ == '__main__':
    write_features('edges_weight_967791600_970383599.net', 'TEST')