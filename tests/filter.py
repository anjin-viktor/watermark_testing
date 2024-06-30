import sys
import shutil
import os
import subprocess

def run(filter, path_source, path_output):
    if shutil.which("ffmpeg") is None:
        print("Error: ffmpeg executable is not Found")
        return -1

    subprocess.call(["ffmpeg", "-y", "-i", path_source, "-vf", filter, path_output], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("`path_source` and `path_output` arguments expected")
        exit(1)

    run("dctdnoiz=s=10", sys.argv[1], sys.argv[2])
#    run("unsharp=3:3:-0.5:3:3:-0.5", sys.argv[1], sys.argv[2])