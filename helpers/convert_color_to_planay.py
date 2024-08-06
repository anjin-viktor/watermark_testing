import sys
import os
import subprocess
import shutil
import pathlib

if len(sys.argv) != 3:
    print("`directory_source` and `directory_destination` arguments expected")
    exit(1)

if shutil.which("color_to_gray") is None:
    print("Error: color_to_gray executable is not Found. Compile and copy to path color_to_gray.cpp application from watermark repository")
    exit(2)

pathlib.Path(sys.argv[2]).mkdir(parents=True, exist_ok=True)

directory = os.fsencode(sys.argv[1])

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    src_filename = str(sys.argv[1]) + "/" +  str(filename)
    dst_filename = str(sys.argv[2]) + "/" +str(filename)
    print(src_filename)
    print(dst_filename)
    out = subprocess.run(["color_to_gray", "-i", src_filename, "-o", dst_filename], capture_output=True, text=True)
