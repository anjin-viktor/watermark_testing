import subprocess

eblind_exe = "/home/user/test/watermark_performance/watermarks/project/apps/eblind_dlc"

levels = [0.005, 0.006, 0.007, 0.0085, 0.01, 0.0135, 0.015, 0.0175, 0.02, 0.0225, 0.025, 0.0275, 0.03, 0.035, 0.04, 0.045, 0.05, 0.06, 0.07, 0.085, 0.1, 0.11, 0.12, 0.135, 0.15, 0.175, 0.2, 0.225, 0.25, 0.3]


def gen_reference(path_source, path_output):
    subprocess.call([eblind_exe, "--gen_reference", "--reference_max=255", "--in=" + path_source, "--out=" + path_output])

def embed(path_source, path_reference, path_output, level):
    subprocess.call([eblind_exe, "--embed", "--in=" + path_source, "--reference=" + path_reference, "--out=" + path_output, "--alpha=" + str(levels[level])])

def detect(path, path_reference):
    out = subprocess.run([eblind_exe, "--detect", "--in=" + path, "--reference=" + path_reference], capture_output=True, text=True)
    if "TRUE" in out.stdout:
        return True
    else:
        return False

if __name__ == "__main__":
    gen_reference("agriculture-hd.jpg", "reference.bmp")
    embed("agriculture-hd.jpg", "reference.bmp", "watermarked.png", 10)
    print(detect("watermarked.png", "reference.bmp"))
    print(detect("agriculture-hd.jpg", "reference.bmp"))
