""" This file is for performing the MLP
"""
from sklearn import linear_model
from sklearn import cross_validation
import numpy as np
import os
import sys

FEATURE_FILENAMES = ['TargetVals.txt', 'CommonNeighbor.txt', 'IDegree.txt', 'IPageRank.txt', 'IVolume.txt', 'JaccardCoefficient.txt', 'JDegree.txt', 'JPageRank.txt', 'JVolume.txt', 'PropFlow.txt', 'RootedPageRank.txt'] # lines: (from to target f1 f2)
# All features are expected to be lines of the format (from, to, feature_value)
# target_vals is lines of the format (from, to, target_value)
# These features are all calculated for a given delta_x and delta_y

def load_files(window, next_window):
    deltasecs = int(window.split('_')[-1]) - int(window.split('_')[-2])
    NUM_EXAMPLES = sum(1 for line in open('./%s/TargetVals.txt' % (window)))
    targets = np.zeros(NUM_EXAMPLES)
    print 'We have:', NUM_EXAMPLES, 'examples'
    print 'We have:', len(FEATURE_FILENAMES), 'features'
    X = np.zeros((NUM_EXAMPLES, len(FEATURE_FILENAMES)))
    lookupMap = {}
    col = 0
    window_feature_filenames = ['%s/%s' % (window, ff) for ff in FEATURE_FILENAMES]
    for feature_filename in FEATURE_FILENAMES:
        with open(window + '/' + feature_filename, 'r') as f:
            row = 0
            for line in f:
                split_line = line.split(' ')
                lookupMap[row] = (split_line[0], split_line[1])
                X[row][col] = float(split_line[2].strip()) # must have only one feature
                row += 1

            col += 1

    with open(next_window + '/TargetVals.txt', 'r') as f:
        row = 0
        for line in f:
            split_line = line.split(' ')
            if (split_line[0], split_line[1]) in lookupMap.values():
                targets[row] = float(split_line[2].strip())
                row += 1

    return X, targets, lookupMap

def process_window_dir(window_dir):
    windows = [name for name in os.listdir(window_dir) if os.path.isdir(os.path.join(window_dir, name))]
    for i, window in enumerate(windows):
        if i == len(windows) - 1: continue
        X, y, lookupMap = load_files(window_dir + '/' + window, window_dir + '/' + windows[i+1])

        #print X
        #print y
        print sum(y)

        # K-fold cross_validation
        kf = cross_validation.KFold(X.shape[1], n_folds=4)

        # clf = linear_model.LinearRegression()
        # clf.fit(X[0:30], y[0:30])
        # print 'R^2 (first 30)', clf.score(X[31:], y[31:])

        for train_index, test_index in kf:
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            clf = linear_model.LinearRegression()
            clf.fit(X_train, y_train)
            print 'R^2 of', clf.score(X_test, y_test)

if __name__ == '__main__':
    process_window_dir(sys.argv[1])
