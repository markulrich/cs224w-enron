from subprocess import Popen, call

def write_features(network_file_name, name):
    # TODO originally 'PropFlow_5', 'IPageRank_D_0.85', 'JPageRank_D_0.85', 'RootedPageRank_D_0.15'
    PREDICTORS = ['IDegree', 'JDegree', 'IVolume', 'JVolume', 'CommonNeighbor', 'JaccardCoefficient', 'AdamicAdar', 'PropFlow_5', 'IPageRank', 'JPageRank', 'RootedPageRank']
    dirName = name
    call(['rm', '-r', dirName])
    call(['mkdir', dirName])
    parr = []; outarr = []
    for pred in PREDICTORS:
        out = open(dirName + '/temp_' + pred, 'w')
        parr.append(Popen(['./LPmade/netlib/bin/predict', '-f', network_file_name, PREDICTORS[0]], stdout=out))
        outarr.append(out)
    for p in parr:
        p.wait()
    for out in outarr:
        out.close()

if __name__ == '__main__':
    write_features('./LPmade/wd/condmat/net/UNSUPERVISED.net', 'TEST')