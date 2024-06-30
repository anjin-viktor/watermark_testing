import os
import csv

from concurrent.futures import ThreadPoolExecutor
from watermarks import eblind_dlc
from utils import psnr
from utils import wmaf
from pathlib import Path
from tests import filter
from tests import transcode

def testImage(input_filename, level):
    filename = Path(input_filename)
    filename_wo_ext = filename.with_suffix('')

    reference_name = "tmp/reference_" + str(level) + "_" +  str(filename_wo_ext) + ".bmp"
    output_name = "tmp/out_" + str(level) + "_" + str(filename_wo_ext) + ".bmp"

    input_file = "images/" + input_filename

    eblind_dlc.gen_reference(input_file, reference_name)
    eblind_dlc.embed(input_file, reference_name, output_name, level)
    result = eblind_dlc.detect(output_name, reference_name)

    dctdnoiz_5_name = "tmp/filter_dctdnoiz_5_" + str(level) + "_" + str(filename_wo_ext) + ".bmp"
    filter.run("dctdnoiz=s=5", output_name, dctdnoiz_5_name)
    result_dctdnoiz_5 = eblind_dlc.detect(dctdnoiz_5_name, reference_name)

    dctdnoiz_10_name = "tmp/filter_dctdnoiz_10_" + str(level) + "_" + str(filename_wo_ext) + ".bmp"
    filter.run("dctdnoiz=s=10", output_name, dctdnoiz_10_name)
    result_dctdnoiz_10 = eblind_dlc.detect(dctdnoiz_10_name, reference_name)

    unsharp_name = "tmp/unsharp_blur_" + str(level) + "_" + str(filename_wo_ext) + ".bmp"
    filter.run("unsharp=3:3:-0.5:3:3:-0.5", output_name, unsharp_name)
    result_unsharp = eblind_dlc.detect(unsharp_name, reference_name)

    sharp_name = "tmp/unsharp_sharp_" + str(level) + "_" + str(filename_wo_ext) + ".bmp"
    filter.run("unsharp=3:3:0.5:3:3:0.5", output_name, sharp_name)
    result_sharp = eblind_dlc.detect(sharp_name, reference_name)

    scale_name = "tmp/scale_75" + str(level) + "_" + str(filename_wo_ext) + ".bmp"
    filter.run("scale=iw*.75:-1", output_name, scale_name)
    reference_scale_name = "tmp/reference_scale_" + str(level) + "_" +  str(filename_wo_ext) + ".bmp"
    filter.run("scale=iw*.75:-1", reference_name, reference_scale_name)
    result_scale = eblind_dlc.detect(scale_name, reference_scale_name)

    crop_name = "tmp/crop_75" + str(level) + "_" + str(filename_wo_ext) + ".bmp"
    filter.run("crop=iw*.75:ih*.75", output_name, crop_name)
    reference_crop_name = "tmp/reference_crop_" + str(level) + "_" +  str(filename_wo_ext) + ".bmp"
    filter.run("crop=iw*.75:ih*.75", reference_name, reference_crop_name)
    result_crop = eblind_dlc.detect(crop_name, reference_crop_name)

    transcode_1_name = "tmp/transcode_1_" + str(level) + "_" + str(filename_wo_ext) + ".bmp"
    transcode.run("mjpeg", ["-qmin", "1", "-qmax", "1"], output_name, transcode_1_name)
    transcode_1 = eblind_dlc.detect(transcode_1_name, reference_name)

    transcode_25_name = "tmp/transcode_25_" + str(level) + "_" + str(filename_wo_ext) + ".bmp"
    transcode.run("mjpeg", ["-qmin", "25", "-qmax", "25"], output_name, transcode_25_name)
    transcode_25 = eblind_dlc.detect(transcode_25_name, reference_name)

    transcode_45_name = "tmp/transcode_45_" + str(level) + "_" + str(filename_wo_ext) + ".bmp"
    transcode.run("mjpeg", ["-qmin", "45", "-qmax", "45"], output_name, transcode_45_name)
    transcode_45 = eblind_dlc.detect(transcode_45_name, reference_name)

    psnr_watermark = psnr.get_score(input_file, output_name)
    psnr_dctdnoiz_5 = psnr.get_score(input_file, dctdnoiz_5_name)
    psnr_dctdnoiz_10 = psnr.get_score(input_file, dctdnoiz_10_name)
    psnr_unsharp = psnr.get_score(input_file, unsharp_name)
    psnr_sharp = psnr.get_score(input_file, sharp_name)
    psnr_transcode_1 = psnr.get_score(input_file, transcode_1_name)
    psnr_transcode_25 = psnr.get_score(input_file, transcode_25_name)
    psnr_transcode_45 = psnr.get_score(input_file, transcode_45_name)

    wmaf_watermark = wmaf.get_score(input_file, output_name)
    wmaf_dctdnoiz_5 = wmaf.get_score(input_file, dctdnoiz_5_name)
    wmaf_dctdnoiz_10 = wmaf.get_score(input_file, dctdnoiz_10_name)
    wmaf_unsharp = wmaf.get_score(input_file, unsharp_name)
    wmaf_sharp = wmaf.get_score(input_file, sharp_name)
    wmaf_transcode_1 = wmaf.get_score(input_file, transcode_1_name)
    wmaf_transcode_25 = wmaf.get_score(input_file, transcode_25_name)
    wmaf_transcode_45 = wmaf.get_score(input_file, transcode_45_name)

    os.remove(reference_name)
    os.remove(output_name)
    os.remove(dctdnoiz_5_name)
    os.remove(dctdnoiz_10_name)
    os.remove(unsharp_name)
    os.remove(sharp_name)
    os.remove(scale_name)
    os.remove(reference_scale_name)
    os.remove(reference_crop_name)
    os.remove(transcode_1_name)
    os.remove(transcode_25_name)
    os.remove(transcode_45_name)

    results = [result, result_dctdnoiz_5, result_dctdnoiz_10, result_unsharp, result_sharp, result_scale, result_crop, transcode_1, transcode_25, transcode_45]
    psnr_scores = [psnr_watermark, psnr_dctdnoiz_5, psnr_dctdnoiz_10, psnr_unsharp, psnr_sharp, psnr_transcode_1, psnr_transcode_25, psnr_transcode_45]
    wmaf_scores = [wmaf_watermark, wmaf_dctdnoiz_5, wmaf_dctdnoiz_10, wmaf_unsharp, wmaf_sharp, wmaf_transcode_1, wmaf_transcode_25, wmaf_transcode_45]

    return [results, psnr_scores, wmaf_scores]

levels = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]

os.makedirs("tmp", exist_ok=True)

csvfile = open('eblind_dlc.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csvfile)
writer.writerow(["W/o modifications", "DCT denoise stretch 5", "DCT denoise stretch 10", "Blurring", "Sharping", "Scaling to 3/4", "Cropping to 3/4", "JPEG Transcoding q=1", "JPEG Transcoding q=25", "JPEG Transcoding q=45"])

csvfilePSNR = open('eblind_dlc_psnr.csv', 'w', newline='', encoding='utf-8')
writerPSNR = csv.writer(csvfilePSNR)
writerPSNR.writerow(["W/o modifications", "DCT denoise stretch 5", "DCT denoise stretch 10", "Blurring", "Sharping", "JPEG Transcoding q=1", "JPEG Transcoding q=25", "JPEG Transcoding q=45"])

csvfileWMAF = open('eblind_dlc_wmaf.csv', 'w', newline='', encoding='utf-8')
writerWMAF = csv.writer(csvfileWMAF)
writerWMAF.writerow(["W/o modifications", "DCT denoise stretch 5", "DCT denoise stretch 10", "Blurring", "Sharping", "JPEG Transcoding q=1", "JPEG Transcoding q=25", "JPEG Transcoding q=45"])

threadPool = ThreadPoolExecutor()

for level in levels:
    directory = os.fsencode("images/")

    cnt = 0
    futures = [];
    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        future = threadPool.submit(testImage, filename, level)
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

    writer.writerow(results)
    writerPSNR.writerow(scores_psnr)
    writerWMAF.writerow(scores_wmaf)
