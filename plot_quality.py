# -*- coding: cp1251 -*-

import matplotlib.pyplot as plt
import numpy as np
import sys

from matplotlib import cm
import csv
from array import array

Xv = []
watermark = []
DCT5 = []
DCT10 = []
Blurring = []
Sharping = []
JPEG_1 = []
JPEG_25 = []
JPEG_45 = []


idx = 0
if len(sys.argv) != 2:
    print("`path_to_csv` argument expected")
    exit(1)

with open(sys.argv[1]) as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        if idx == 0:
           Headers = row
        else:
            watermark.append(float(row[0]))
            DCT5.append(float(row[1]))
            DCT10.append(float(row[2]))
            Blurring.append(float(row[3]))
            Sharping.append(float(row[4]))
            JPEG_1.append(float(row[5]))
            JPEG_25.append(float(row[6]))
            JPEG_45.append(float(row[7]))
        idx += 1

watermark = np.array(watermark)
DCT5 = np.array(DCT5)
DCT10 = np.array(DCT10)
Blurring = np.array(Blurring)
Sharping = np.array(Sharping)
JPEG_1 = np.array(JPEG_1)
JPEG_25 = np.array(JPEG_25)
JPEG_45 = np.array(JPEG_45)


#X = np.linspace(0, len(watermark), len(watermark))
X = [0.005, 0.006, 0.007, 0.0085, 0.01, 0.0135, 0.015, 0.0175, 0.02, 0.0225, 0.025, 0.0275, 0.03, 0.035, 0.04, 0.045, 0.05, 0.06, 0.07, 0.085, 0.1, 0.11, 0.12, 0.135, 0.15, 0.175, 0.2, 0.225, 0.25, 0.3]

fig, ax = plt.subplots(1, 1)

ax.plot(X, watermark)
ax.plot(X, DCT5)
ax.plot(X, DCT10)
ax.plot(X, Blurring)
ax.plot(X, Sharping)
ax.plot(X, JPEG_1)
ax.plot(X, JPEG_25)
ax.plot(X, JPEG_45)

#ax.set_ylabel('PSNR')
ax.set_ylabel('WMAF')
ax.set_xlabel('Value of \u03B1 watermark embedding coefficient')
ax.legend(Headers)
print(Headers)


plt.show()
