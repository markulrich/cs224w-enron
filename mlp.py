""" This file is for performing the MLP
"""
from sklearn import linear_model
from sklearn import cross_validation
import numpy as np

FEATURE_FILENAME = ['TargetVals.txt'] # lines: (from to target f1 f2)
# All features are expected to be lines of the format (from, to, feature_value)
# target_vals is lines of the format (from, to, target_value)
# These features are all calculated for a given delta_x and delta_y

X, y, lookupMap = load_files(feature_filenames)

# K-fold cross_validation
kf = cross_validation.KFold(X.shape[1], n_folds=4)

for train_index, test_index in kf:
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    clf = linear_model.LinearRegression()
    clf.fit(X_train, y_train)
    print 'R^2 of', clf.score(X_test, y_test)

def load_files(feature_filenames):
    targets = np.array(NUM_EXAMPLES)
    X = np.array(NUM_EXAMPLES)
    lookupMap = {}
    with open(FEATURE_FILENAME, 'r') as f:
        i = 0
        for line in f:
            split_line = line.split(' ')
            lookupMap[i] = (split_line[0], split_line[1])
            X[i] = np.array([float(x) for x in split_line[3:]]) # must have at least one feature
            targets[i] = float(split_line[2])
            i += 1

    return X, targets, lookupMap
