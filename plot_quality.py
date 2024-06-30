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


X = np.linspace(0, len(watermark), len(watermark))

fig, ax = plt.subplots(1, 1)

ax.plot(X, watermark)
ax.plot(X, DCT5)
ax.plot(X, DCT10)
ax.plot(X, Blurring)
ax.plot(X, Sharping)
ax.plot(X, JPEG_1)
ax.plot(X, JPEG_25)
ax.plot(X, JPEG_45)

ax.set_ylabel('PSNR')
#ax.set_ylabel('WMAF')
ax.set_xlabel('Value of \u03B1 watermark embedding coefficient')
ax.legend(Headers)
print(Headers)


plt.show()
