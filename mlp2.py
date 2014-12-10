__author__ = 'mark'

""" This file is for performing the MLP
"""
from sklearn import linear_model
from sklearn import cross_validation
import numpy as np
import os
import sys
from sklearn.metrics import r2_score
from sklearn.preprocessing import scale

#SUB_FEATURES = ['EdgeWeight.txt', 'JPageRank.txt', 'PropFlow.txt', 'IVolume.txt', 'RootedPageRank.txt']
FEATURES = ['EdgeWeight.txt', 'CommonNeighbor.txt', 'IDegree.txt', 'IPageRank.txt', 'IVolume.txt', 'JaccardCoefficient.txt', 'JDegree.txt', 'JPageRank.txt', 'JVolume.txt', 'PropFlow.txt', 'RootedPageRank.txt'] # lines: (from to target f1 f2)
# All features are expected to be lines of the format (from, to, feature_value)
# target_vals is lines of the format (from, to, target_value)
# These features are all calculated for a given delta_x and delta_y
NLP_FEATURES = ['SentSum', 'LinesSum', 'MC1Sum', 'MC2Sum', 'MC3Sum', 'MC4Sum', 'MC5Sum', 'MC6Sum', 'SentMean', 'LinesMean', 'MC1Mean', 'MC2Mean', 'MC3Mean', 'MC4Mean', 'MC5Mean', 'MC6Mean']
NLP_AND_MC_FEATURES = len(NLP_FEATURES)
FEATURE_NAMES = FEATURES + NLP_FEATURES
BEST_FEATURES = ['EdgeWeight.txt',
                 'PropFlow.txt',
                 'RootedPageRank.txt',
                 'LinesMean',
                 'MC2Mean',
                 'SentMean',
                 'MC6Mean',
                 'JPageRank.txt',
                 'MC1Mean',
                 'MC5Mean',
                 'IVolume.txt',
                 'CommonNeighbor.txt',
                 'JaccardCoefficient.txt',
                 'JVolume.txt',
                 'JDegree.txt',
                 'MC4Mean',
                 'IDegree.txt',
                 'MC3Mean',
                 'IPageRank.txt']

def load_files(window):
    features = FEATURES
    NUM_EXAMPLES = sum(1 for line in open('./%s/EdgeWeight.txt' % (window)))
    targets = np.zeros(NUM_EXAMPLES)
    print 'We have:', NUM_EXAMPLES, 'examples'
    print 'We have:', len(features) + NLP_AND_MC_FEATURES, 'features'
    X = np.zeros((NUM_EXAMPLES, len(features) + NLP_AND_MC_FEATURES))
    lookupMap = {}
    col = 0
    window_feature_filenames = ['%s/%s' % (window, ff) for ff in features]
    for feature_filename in FEATURES:
        with open(window + '/' + feature_filename, 'r') as f:
            row = 0
            for line in f:
                split_line = line.split(' ')
                lookupMap[(split_line[0], split_line[1])] = row
                X[row][col] = float(split_line[2].strip()) # must have only one feature
                row += 1

            col += 1

    # Process EdgeAttrs.txt
    with open(window + '/' + 'EdgeAttrs.txt', 'r') as f:
        row = 0
        for line in f:
            split_line = line.split(' ')
            lookupMap[(split_line[0], split_line[1])] = row
            # Remaining are:
            # SentimentSum LinesSum MC1SUM ... MCNSUM SentimentMean LinesMean MC1MEAN ... MCNMEAN
            for i in xrange(1, NLP_AND_MC_FEATURES + 1):
                X[row][-i] = float(split_line[-i].strip())
            row += 1

    with open(window + '/Labels.txt', 'r') as f:
        for line in f:
            split_line = line.split(' ')
            if (split_line[0], split_line[1]) in lookupMap:
                targets[lookupMap[(split_line[0], split_line[1])]] = float(split_line[2].strip())

    return X, targets

def process_window_dir(window_dir, model, features, X, y, kf):
    print 'Processing', window_dir
    alphas = [0.025]
    only_feature_selection = False
    X = X[:,[FEATURE_NAMES.index(f) for f in features]]
    X = scale(X)

    from sklearn.feature_selection import SelectKBest, f_regression

    # featureSelector = SelectKBest(score_func=f_regression,k=len(FEATURE_NAMES))
    # featureSelector.fit(X,y)
    # print 'Selected features', [FEATURE_NAMES[i] for i in list(featureSelector.get_support(indices=True))]

    if only_feature_selection:
        baseline_mean(X,y)
        baseline_zero(X,y)

        F, pval = f_regression(X, y)
        for i,f in enumerate(F):
            if i < len(FEATURES):
                name = FEATURES[i]
            else:
                name = NLP_FEATURES[i-11]
            print 'F-Statistic for %s is %f with p-value %f' % (name, f, pval[i])

        return None

    else:
        scores = []
        # print 'sum of y is %d' % sum(y)
        # clf = model()
        # clf.fit(X[:30], y[:30])
        # print 'small score is %g' % clf.score(X[30:60], y[30:60])

        # K-fold cross_validation
        for train_index, test_index in kf:
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            for alpha in alphas:
                clf = model()
                clf.set_params(alpha=alpha)
                clf.fit(X_train, y_train)
                score = clf.score(X_test, y_test)
                scores.append(score)
                # print '{} score is {} when alpha is {}'.format(model.__name__, score, alpha)
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
    # windows = [name for name in os.listdir(sys.argv[1])]
    #
    # print 'Windows in', sys.argv[1], 'are', windows
    #
    # for f in windows:
    #     scores = process_window_dir(sys.argv[1] + '/' + f, linear_model.Ridge, FEATURES)
    #     if scores != None and None not in scores:
    #         res = np.mean(scores)
    #         var = np.var(scores)
    #         print 'res is %f with var %f' % (res, var)
    #     else:
    #         print 'No stats as this was only for feature engineering.'
    X, y = load_files('windows/attrdays30/time1')
    kf = cross_validation.KFold(X.shape[0], n_folds=10, shuffle=True)
    NLP_FEATS = ['EdgeWeight.txt', 'SentMean', 'LinesMean', 'MC1Mean', 'MC2Mean', 'MC3Mean', 'MC4Mean', 'MC5Mean', 'MC6Mean']
    GRAPH_FEATS = ['EdgeWeight.txt', 'CommonNeighbor.txt', 'IDegree.txt', 'IPageRank.txt', 'IVolume.txt', 'JaccardCoefficient.txt', 'JDegree.txt', 'JPageRank.txt', 'JVolume.txt', 'PropFlow.txt', 'RootedPageRank.txt']
    GRAPH_FEATS = FEATURES
    BEST_FEATS = ['EdgeWeight.txt',
                     'PropFlow.txt',
                     'RootedPageRank.txt',
                     'LinesMean',
                     'MC2Mean',
                     'SentMean',
                     'MC6Mean',
                     'JPageRank.txt',
                     'MC1Mean',
                     'MC5Mean',
                     'IVolume.txt',
                     'CommonNeighbor.txt',
                     'JaccardCoefficient.txt',
                     'JVolume.txt',
                     'JDegree.txt',
                     'MC4Mean',
                     'IDegree.txt',
                     'MC3Mean',
                     'IPageRank.txt']

    scores = process_window_dir('windows/attrdays30/time1', linear_model.Ridge, BEST_FEATS, X, y, kf)
    print 'With BEST_FEATS with %f with var %f' % (np.mean(scores), np.var(scores))

    scores = process_window_dir('windows/attrdays30/time1', linear_model.Ridge, GRAPH_FEATS, X, y, kf)
    print 'With GRAPH_FEATS with %f with var %f' % (np.mean(scores), np.var(scores))

    scores = process_window_dir('windows/attrdays30/time1', linear_model.Ridge, NLP_FEATS, X, y, kf)
    print 'With NLP_FEATS with %f with var %f' % (np.mean(scores), np.var(scores))
