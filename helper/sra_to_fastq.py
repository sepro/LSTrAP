#!/usr/bin/env python3
import subprocess
import sys, os, re  
import random

if len(sys.argv) != 3:
    print("Error with arguments. Usage ./sra_to_fastq.py <INPUT_DIR> <OUTPUT_DIR>")
    quit()

input_dir = sys.argv[1]
output_dir = sys.argv[2]

# Convert .sra file to fastq
sra_files = [f for f in os.listdir(input_dir)]
random.shuffle(sra_files)
for sra_file in sra_files:
    if sra_file.endswith('.sra'):
        path = os.path.join(input_dir, sra_file)

        output_a = os.path.join(output_dir, sra_file.replace('.sra', '.fastq.gz'))
        output_b = os.path.join(output_dir, sra_file.replace('.sra', '_1.fastq.gz'))

        if not (os.path.exists(output_a) or os.path.exists(output_b)):
            print("Converting", path)
            subprocess.call(["fastq-dump", "--gzip", "--skip-technical", "--readids", "--dumpbase", "--split-3", path, "-O", output_dir])
        else:
            print("File exists, skipping", path)


