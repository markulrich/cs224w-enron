import numpy as np
import math

with open('degdistOut.tab') as f:
    data = []
    for line in f:
        line = line.rstrip().split('\t')
        data.append(float(line[-1]))

    x_min = 7.0

    d_vals = [v for v in data if v >= x_min]

    print 1.0 + len(d_vals) * ((sum([math.log(v / x_min) for v in d_vals])) ** -1)
