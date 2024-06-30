import sys
import shutil
import os
import subprocess

def run(codec, parameters, path_source, path_output):
    if shutil.which("ffmpeg") is None:
        print("Error: ffmpeg executable is not Found")
        return -1

    subprocess.call(["ffmpeg", "-y", "-i", path_source, "-vcodec", codec] + parameters + [path_output], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("`path_source` argument is expected")
        exit(1)

    run("mjpeg", ["-qmin", "1", "-qmax", "1" ], sys.argv[1], "out_1.jpg")
    run("mjpeg", ["-qmin", "45", "-qmax", "45" ], sys.argv[1], "out_45.jpg")
