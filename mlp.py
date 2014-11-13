""" This file is for performing the MLP
"""
from multiprocessing import Pool
from sklearn import linear_model
from sklearn import cross_validation
from sklearn.ensemble import RandomForestRegressor, BaggingRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.feature_selection import f_regression, SelectKBest
from sklearn.svm import SVR
import sklearn
import numpy as np
import os
import sys

AVAIL_FEATURES = ['TargetVals.txt', 'CommonNeighbor.txt', 'IDegree.txt', 'IPageRank.txt', 'IVolume.txt', 'JaccardCoefficient.txt', 'JDegree.txt', \
            'JPageRank.txt', 'JVolume.txt', 'PropFlow.txt', 'RootedPageRank.txt'] # lines: (from to target f1 f2)

GOOD_IND = [0,1,4,6,7,9,10]
#GOOD_IND = [0,7,9,10]
FEATURES = [feature for i,feature in enumerate(AVAIL_FEATURES) if i in GOOD_IND]

#TODO: recenter data!

# All features are expected to be lines of the format (from, to, feature_value)
# target_vals is lines of the format (from, to, target_value)
# These features are all calculated for a given delta_x and delta_y

def load_files(window, next_window, features):
    deltasecs = int(window.split('_')[-1]) - int(window.split('_')[-2])
    NUM_EXAMPLES = sum(1 for line in open('./%s/TargetVals.txt' % (window)))
    targets = np.zeros(NUM_EXAMPLES)
    print window, next_window
    print 'We have:', NUM_EXAMPLES, 'examples'
    print 'We have:', len(features), 'features'
    X = np.zeros((NUM_EXAMPLES, len(features)))
    lookupMap = {}
    col = 0
    window_feature_filenames = ['%s/%s' % (window, ff) for ff in features]
    for feature_filename in features:
        with open(window + '/' + feature_filename, 'r') as f:
            row = 0
            for line in f:
                split_line = line.split(' ')
                lookupMap[(split_line[0], split_line[1])] = row
                X[row][col] = float(split_line[2].strip()) # must have only one feature
                row += 1

            col += 1

    with open(next_window + '/TargetVals.txt', 'r') as f:
        for line in f:
            split_line = line.split(' ')
            if (split_line[0], split_line[1]) in lookupMap:
                targets[lookupMap[(split_line[0], split_line[1])]] = float(split_line[2].strip())

    return X, targets

def process_window_dir(window_dir, model, features):
    # TODO this method breaks if there are timestamps with lexographic and numerical order mismatch
    # TODO: update to mark's new format of data
    windows = [name for name in os.listdir(window_dir) if os.path.isdir(os.path.join(window_dir, name))]
    scores = []
    #X = np.empty((0,len(FEATURES)), float)
    #y = np.empty((0,), float)
    F = np.zeros((1,len(FEATURES)))
    for i, window in enumerate(windows):
        if i == len(windows) - 1: continue
        X, y = load_files(window_dir + '/' + window, window_dir + '/' + windows[i+1], features)

        #X = np.append(X, X_new, axis=0)
        #y = np.append(y, y_new, axis=0)

        #F_new, _ = f_regression(X, y, center=True)
        #F = F + F_new
        b = SelectKBest(f_regression, k=5)
        b.fit(X, y)
        print b
        print b.scores_
        print b.pvalues_
        print b.get_support()



        # # K-fold cross_validation
        # kf = cross_validation.KFold(X.shape[0], n_folds=4)
        # for train_index, test_index in kf:
        #     X_train, X_test = X[train_index], X[test_index]
        #     y_train, y_test = y[train_index], y[test_index]
        #     clf = model()
        #     clf.fit(X_train, y_train)
        #     score = clf.score(X_test, y_test)
        #     print '{} score is {}'.format(model.__name__, score)
        #     scores.append(score)
    #print F / len(windows) - 1
    return scores

if __name__ == '__main__':
    def call_pwd(model):
        scores = process_window_dir(sys.argv[1], model, FEATURES)
        return model.__name__, np.mean(scores), np.std(scores)

    scores = process_window_dir(sys.argv[1], SVR, FEATURES)
    print '### PRINTING FINAL SCORES ###'
    for r in scores:
        print(r)
    if len(sys.argv) > 2:
        with open(sys.argv[2], 'w') as f:
            f.write('{}\n'.format(r))
