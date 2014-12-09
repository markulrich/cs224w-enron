""" This file is for performing the MLP
"""
from sklearn import linear_model
from sklearn import cross_validation
import numpy as np
import os
import sys
from sklearn.metrics import r2_score

SUB_FEATURES = ['EdgeWeight.txt', 'JPageRank.txt', 'PropFlow.txt', 'IVolume.txt', 'RootedPageRank.txt']
FEATURES = ['EdgeWeight.txt', 'CommonNeighbor.txt', 'IDegree.txt', 'IPageRank.txt', 'IVolume.txt', 'JaccardCoefficient.txt', 'JDegree.txt', 'JPageRank.txt', 'JVolume.txt', 'PropFlow.txt', 'RootedPageRank.txt'] # lines: (from to target f1 f2)
# All features are expected to be lines of the format (from, to, feature_value)
# target_vals is lines of the format (from, to, target_value)
# These features are all calculated for a given delta_x and delta_y

def load_files(window, features):
    deltasecs = int(window.split('_')[-1]) - int(window.split('_')[-2])
    NUM_EXAMPLES = sum(1 for line in open('./%s/EdgeWeight.txt' % (window)))
    targets = np.zeros(NUM_EXAMPLES)
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

    with open(window + '/Labels.txt', 'r') as f:
        for line in f:
            split_line = line.split(' ')
            if (split_line[0], split_line[1]) in lookupMap:
                targets[lookupMap[(split_line[0], split_line[1])]] = float(split_line[2].strip())

    return X, targets

def process_window_dir(window_dir, model, features):
    # TODO this method breaks if there are timestamps with lexographic and numerical order mismatch
    windows = [name for name in os.listdir(window_dir)]
    scores = []
    for i, window in enumerate(windows):
        X, y = load_files(window_dir + '/' + window, features)

        print 'sum of y is %d' % sum(y)
        clf = model()
        clf.fit(X[:30], y[:30])
        print 'small score is %g' % clf.score(X[30:60], y[30:60])

        # K-fold cross_validation
        kf = cross_validation.KFold(X.shape[0], n_folds=4)
        for train_index, test_index in kf:
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            clf = model()
            clf.fit(X_train, y_train)
            score = clf.score(X_test, y_test)
            print '{} score is {}'.format(model.__name__, score)
            scores.append(score)
    return scores

def baseline_mean(test_x, test_y):
    mean = 0.0
    for x in test_x:
        mean += x[0]

    mean /= len(test_x)
    print 'Mean baseline r^2 score of', r2_score(test_y, [mean] * len(test_x))

def baseline_zero(test_x, test_y):
    print 'Zero baseline r^2 score of', r2_score(test_y, [0.0] * len(test_x))


if __name__ == '__main__':
    folders = [name for name in os.listdir(sys.argv[1])]

    points = {}
    for f in folders:
        names = f.split(' ')
        past = int(names[0])
        future = int(names[1])
        print 'computing %d %d' % (past, future)
        scores = process_window_dir(sys.argv[1] + '/' + f, linear_model.LinearRegression, SUB_FEATURES)
        res = np.mean(scores)
        print 'res is %g' % res
        points[(past, future)] = res
    import pickle
    with open('timeDeltaForGraph.pickle', 'w') as out:
        pickle.dump(points, out)
