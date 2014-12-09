from subprocess import Popen, call
import os
import collections
from collections import defaultdict
from edges_by_timestamp import strtotime, TIME_FORMAT

PREDICT_BIN_PATH = './LPmade/netlib/bin/predict'
# TODO originally 'PropFlow_5', 'IPageRank_D_0.85', 'JPageRank_D_0.85', 'RootedPageRank_D_0.15'
PREDICTORS = ['IDegree', 'JDegree', 'IVolume', 'JVolume', 'CommonNeighbor', 'JaccardCoefficient', 'AdamicAdar', 'PropFlow', 'IPageRank', 'JPageRank', 'RootedPageRank']

def make_if_needed():
    if not os.path.isfile(PREDICT_BIN_PATH):
        print('MAKING PREDICT BINARY, THIS WILL ONLY RUN THE FIRST TIME. WARNINGS EXPECTED')
        call('make', cwd = './LPmade/netlib/')

def genLabelFile(network_file_name, dirName, output_name='/EdgeWeight.txt'):
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
    with open(dirName + output_name, 'w') as out:
        for src in xrange(numNodes):
            for dst in xrange(numNodes):
                out.write('{} {} {}\n'.format(intToExt[src], intToExt[dst], weights[(src, dst)]))
    return intToExt, numNodes

def getEdgesToEmail(window):
    startTime = strtotime(window[0].strftime(TIME_FORMAT))
    endTime = strtotime(window[1].strftime(TIME_FORMAT))
    edgesToEmail = defaultdict(list)
    with open('edges.txt') as edgesf:
        for line in edgesf:
            tokens = line.split(',')
            date = strtotime(tokens[0])
            if date >= startTime and date < endTime:
                src = int(tokens[1])
                dst = int(tokens[2])
                email = tokens[3]
                edgesToEmail[(src, dst)] += [email.strip()]
    return edgesToEmail

def getEmailToNlp():
    nFeats = 2
    emailToNlp = defaultdict(lambda: [0] * nFeats)
    with open('nlp_features.out') as nlpf:
        for line in nlpf:
            tokens = line.split(',')
            feats = (float(tokens[1]), float(tokens[nFeats]))
            emailToNlp[tokens[0]] = feats
    return emailToNlp, nFeats

def getEmailToMc():
    first = True
    with open('message_class.labels') as mcf:
        for line in mcf:
            tokens = line.split(' ')
            if first:
                first = False
                nFeats = len(tokens) - 1
                emailToMc = defaultdict(lambda: [0] * nFeats)
            emailToMc[tokens[0][1:]] = tuple(int(tokens[x]) for x in xrange(1, nFeats + 1))
    return emailToMc, nFeats

# Generates an edge attribute file where each row has the format
# src dest NLP1SUM ... NLPNSUM MC1SUM ... MCNSUM NLP1MEAN ... NLPNMEAN MC1MEAN ... MCNMEAN
def genAttrFiles(dirName, intToExt, numNodes, window):
    edgesToEmail = getEdgesToEmail(window)
    emailToNlp, nNlp = getEmailToNlp()
    emailToMc, nMc = getEmailToMc()

    def summation(data):
        return sum(dat for dat in data)

    def mean(data):
        return 0 if len(data) == 0 else summation(data) / len(data)

    ALGS = [summation, mean]

    with open(dirName + 'EdgeAttrs.txt', 'w') as out:
        for src in xrange(numNodes):
            for dst in xrange(numNodes):
                srcExt = intToExt[src]
                dstExt = intToExt[dst]
                allData = [[emailToNlp[email][i] for email in edgesToEmail[(srcExt, dstExt)]] for i in range(nNlp)] + \
                        [[emailToMc[email][i] for email in edgesToEmail[(srcExt, dstExt)]] for i in range(nMc)]
                featurePoints = [alg(d) for alg in ALGS for d in allData]
                out.write((('{} ' * (2 + len(featurePoints)))[:-1] + '\n').format(srcExt, dstExt, *featurePoints))

def write_features(network_file_name, dirName, window):
    if not os.path.isfile(network_file_name):
        print('Sorry, {} is not a valid file.'.format(network_file_name))
        return
    make_if_needed()
    parr = []; outarr = []
    for pred in PREDICTORS:
        out = open(dirName + '/' + pred + '.txt', 'w')
        parr.append(Popen([PREDICT_BIN_PATH, '-f', network_file_name, pred], stdout=out))
        outarr.append(out)
    intToExt, numNodes = genLabelFile(network_file_name, dirName)
    genAttrFiles(dirName, intToExt, numNodes, window)
    for p in parr:
        p.wait()
    for out in outarr:
        out.close()