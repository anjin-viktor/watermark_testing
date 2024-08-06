# -*- coding: cp1251 -*-

import matplotlib.pyplot as plt
import numpy as np
import sys

from matplotlib import cm
import csv
from array import array

Xv = []

idx = 0
if len(sys.argv) != 2:
    print("`path_to_csv` argument expected")
    exit(1)

scores = []
with open(sys.argv[1]) as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        scores.append(row)
        idx += 1

eblind_dlc = np.array(scores[0], dtype=float)
eblind_dlc_robust = np.array(scores[1], dtype=float)
X = [0, 1, 2, 3, 5, 7, 9, 11, 13, 15, 19, 23, 27, 33]
fig, ax = plt.subplots(1, 1)

ax.plot(X, eblind_dlc)
ax.plot(X, eblind_dlc_robust)

ax.set_ylabel('Watermark detection probability')
ax.set_xlabel('Value of filtering coefficient')

ax.legend(["eblind_dlc", "eblind_dlc_robust"])

plt.show()
