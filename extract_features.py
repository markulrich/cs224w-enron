from subprocess import Popen, call
import os

PREDICT_BIN_PATH = './LPmade/netlib/bin/predict'

def make_if_needed():
    if not os.path.isfile(PREDICT_BIN_PATH):
        print('MAKING PREDICT BINARY, THIS WILL ONLY RUN THE FIRST TIME. WARNINGS EXPECTED')
        call('make', cwd = './LPmade/netlib/')

def write_features(network_file_name, name):
    if not os.path.isfile(network_file_name):
        print('Sorry, {} is not a valid file.'.format(network_file_name))
        return
    make_if_needed()
    # TODO originally 'PropFlow_5', 'IPageRank_D_0.85', 'JPageRank_D_0.85', 'RootedPageRank_D_0.15'
    PREDICTORS = ['IDegree', 'JDegree', 'IVolume', 'JVolume', 'CommonNeighbor', 'JaccardCoefficient', 'AdamicAdar', 'PropFlow', 'IPageRank', 'JPageRank', 'RootedPageRank']
    dirName = name
    if os.path.exists(dirName):
        call(['rm', '-r', dirName])
    call(['mkdir', dirName])
    parr = []; outarr = []
    for pred in PREDICTORS:
        out = open(dirName + '/' + pred + '.txt', 'w')
        parr.append(Popen([PREDICT_BIN_PATH, '-f', network_file_name, pred], stdout=out))
        outarr.append(out)
    for p in parr:
        p.wait()
    for out in outarr:
        out.close()

if __name__ == '__main__':
    write_features('TEST.net', 'TEST')