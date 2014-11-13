import numpy as np
import matplotlib.pyplot as plt

def linRegressionPlot():
    linear_regression_scores = [
        [0.489129194,
        0.324072218,
        0.495957055,
        0.4546415],
        [0.405539516,
        0.474694617,
        0.343540481,
        0.19380063],
        [0.265918935,
        0.258077783,
        0.61781126,
        0.086195646],
        [0.317623497,
        0.069295859,
        0.536542015,
        -0.499596296],
        [-0.070248767,
        0.242454689,
        0.461709805,
        -0.434100414],
        [0.19247657,
        0.64668126,
        0.787905074,
        0.45427875],
        [0.319051024,
        0.402059582,
        0.501890797,
        -0.311936524]
    ]
    for scores in linear_regression_scores:
        np.mean(scores)
        np.std(scores)

    ax = plt.gca()
    plt.errorbar(range(1, len(linear_regression_scores) + 1), [np.mean(s) for s in linear_regression_scores], [np.std(s) for s in linear_regression_scores], linestyle='None', marker='^')
    plt.xlabel('Window Number')
    plt.ylabel(r'$r^2$ Score Using 4-fold Validation')
    plt.xlim([0, len(linear_regression_scores) + 1])
    plt.show()
    print 'Windows of 100 days starting at 1999/05/18'
    print 'Mean is'
    print np.mean([s for scores in linear_regression_scores for s in scores])

def timeDeltaPlot():
    import pickle
    with open('timeDeltaForGraph.pickle') as f:
        pointsDict = pickle.load(f)
    Z = np.zeros(shape=(9, 9))
    for times, val in pointsDict.items():
        Z[times[0], times[1]] = val
    ax = plt.gca()
    plt.xticks(np.arange(2, Z.shape[0])+0.5)
    plt.yticks(np.arange(2, Z.shape[1])+0.5)
    ax.set_xticklabels([2**i for i in range(2, 9)])
    ax.set_yticklabels([2**i for i in range(2, 9)])
    plt.xlabel('Days in Feature Window')
    plt.ylabel('Days in Label Window')
    plt.xlim([2, 9])
    plt.ylim([2, 9])
    plt.pcolor(Z, cmap='PuBu_r')
    plt.colorbar()
    plt.show()

if __name__ == '__main__':
    timeDeltaPlot()