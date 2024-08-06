import os
import csv

from concurrent.futures import ThreadPoolExecutor
from watermarks import eblind_dlc, eblind_dlc_dctdniz_robust
from utils import psnr
from utils import wmaf
from pathlib import Path
from tests import filter

def testImage(input_filename, watermark):
    os.makedirs("tmp", exist_ok=True)
    os.makedirs("tmp/out", exist_ok=True)
    os.makedirs("tmp/reference", exist_ok=True)
    os.makedirs("tmp/filter_dctdnoiz", exist_ok=True)

    filename = Path(input_filename)
    filename_wo_ext = filename.with_suffix('')

    reference_name = "tmp/reference/" + str(filename_wo_ext) + ".bmp"
    output_name = "tmp/out/" + str(filename_wo_ext) + ".bmp"
    input_file = "images/" + input_filename

    if(watermark == eblind_dlc):
        watermark.gen_reference(input_file, reference_name, 7)
    else:
        watermark.gen_reference(input_file, reference_name, 7, 30)
    watermark.embed(input_file, reference_name, output_name)
    result = watermark.detect(output_name, reference_name)

    psnr_watermark = psnr.get_score(input_file, output_name)
    wmaf_watermark = wmaf.get_score(input_file, output_name)

    results = [result]
    psnr_scores = [psnr_watermark]
    wmaf_scores = [wmaf_watermark]

    sigma_values = [1, 2, 3, 5, 7, 9, 11, 13, 15, 19, 23, 27, 33]
    for sigma in sigma_values:
        dctdnoiz_name = "tmp/filter_dctdnoiz/" + str(filename_wo_ext) + "_" + str(sigma) + ".bmp"
        filter.run("dctdnoiz=s="+ str(sigma), output_name, dctdnoiz_name)
        result = watermark.detect(dctdnoiz_name, reference_name)
        psnr_dctdnoiz = psnr.get_score(input_file, dctdnoiz_name)
        wmaf_dctdnoiz = wmaf.get_score(input_file, dctdnoiz_name)

        results.append(result)
        psnr_scores.append(psnr_dctdnoiz)
        wmaf_scores.append(wmaf_dctdnoiz)

        os.remove(dctdnoiz_name)

    os.remove(reference_name)
    os.remove(output_name)

    return [results, psnr_scores, wmaf_scores]

def test_watermark(watermark):
    directory = os.fsencode("images/")
    results = []
    scores_psnr = []
    scores_wmaf = []
    cnt = 0
    threadPool = ThreadPoolExecutor()

    directory = os.fsencode("images/")

    futures = [];
    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        future = threadPool.submit(testImage, filename, watermark)
        futures.append(future)
        cnt = cnt + 1

    results = []
    scores_psnr = []
    scores_wmaf = []

    for future in futures:
        result = future.result()
        if len(results) != len(result[0]):
            results = [0] * len(result[0])
            scores_psnr = [0] * len(result[1])
            scores_wmaf = [0] * len(result[2])

        for i, val in enumerate(result[0]):
            results[i] += int(val)
        for i, val in enumerate(result[1]):
            scores_psnr[i] += int(val)
        for i, val in enumerate(result[2]):
            scores_wmaf[i] += int(val)

    for i, val in enumerate(results):
        results[i] = results[i] / cnt
    for i, val in enumerate(scores_psnr):
        scores_psnr[i] = scores_psnr[i] / cnt
    for i, val in enumerate(scores_wmaf):
        scores_wmaf[i] = scores_wmaf[i] / cnt

    return [results, scores_psnr, scores_wmaf]

csvfile = open('dctdnoiz_robust.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csvfile)
csvfilePSNR = open('dctdnoiz_robust_psnr.csv', 'w', newline='', encoding='utf-8')
writerPSNR = csv.writer(csvfilePSNR)
csvfileWMAF = open('dctdnoiz_robust_wmaf.csv', 'w', newline='', encoding='utf-8')
writerWMAF = csv.writer(csvfileWMAF)

results = test_watermark(eblind_dlc)
writer.writerow(results[0])
writerPSNR.writerow(results[1])
writerWMAF.writerow(results[2])

results = test_watermark(eblind_dlc_dctdniz_robust)
writer.writerow(results[0])
writerPSNR.writerow(results[1])
writerWMAF.writerow(results[2])
