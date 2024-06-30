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

watermark_wmaf = []
DCT5_wmaf = []
DCT10_wmaf = []
Blurring_wmaf = []
Sharping_wmaf = []
JPEG_1_wmaf = []
JPEG_25_wmaf = []
JPEG_45_wmaf = []


Headers = []

idx = 0

if len(sys.argv) != 3:
    print("`path_to_detection_level.csv` and `path_to_wmaf.csv` arguments are expected")
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
            JPEG_1.append(float(row[7]))
            JPEG_25.append(float(row[8]))
            JPEG_45.append(float(row[9]))
        idx += 1

watermark = np.array(watermark)
DCT5 = np.array(DCT5)
DCT10 = np.array(DCT10)
Blurring = np.array(Blurring)
Sharping = np.array(Sharping)
JPEG_1 = np.array(JPEG_1)
JPEG_25 = np.array(JPEG_25)
JPEG_45 = np.array(JPEG_45)

with open(sys.argv[2]) as csvfile:
    idx = 0
    reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        if idx == 0:
           Headers = row
        else:
            watermark_wmaf.append(float(row[0]))
            DCT5_wmaf.append(float(row[1]))
            DCT10_wmaf.append(float(row[2]))
            Blurring_wmaf.append(float(row[3]))
            Sharping_wmaf.append(float(row[4]))
            JPEG_1_wmaf.append(float(row[5]))
            JPEG_25_wmaf.append(float(row[6]))
            JPEG_45_wmaf.append(float(row[7]))
        idx += 1

watermark_wmaf = np.array(watermark_wmaf)
DCT5_wmaf = np.array(DCT5_wmaf)
DCT10_wmaf = np.array(DCT10_wmaf)
Blurring_wmaf = np.array(Blurring_wmaf)
Sharping_wmaf = np.array(Sharping_wmaf)
JPEG_1_wmaf = np.array(JPEG_1_wmaf)
JPEG_25_wmaf = np.array(JPEG_25_wmaf)
JPEG_45_wmaf = np.array(JPEG_45_wmaf)

fig, ax = plt.subplots(1, 1)
X = np.linspace(0, len(watermark), len(watermark))


ax.plot(watermark_wmaf, watermark)
ax.plot(DCT5_wmaf, DCT5)
ax.plot(DCT10_wmaf, DCT10)
ax.plot(Blurring_wmaf, Blurring)
ax.plot(Sharping_wmaf, Sharping)
ax.plot(JPEG_1_wmaf, JPEG_1)
ax.plot(JPEG_25_wmaf, JPEG_25)
ax.plot(JPEG_45_wmaf, JPEG_45)

ax.set_ylabel('Watermark detection probability')
ax.set_xlabel('PSNR between the original and filtered watermarked images')
ax.legend(Headers)

plt.show()
