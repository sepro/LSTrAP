#!/usr/bin/env python3
import subprocess
import sys
import os
import random

if len(sys.argv) != 3:
    print("Error with arguments. Usage ./get_sra_ip.py <INPUT> <OUTPUT_DIR> <ASPERA_KEY>")
    quit()

input_list = sys.argv[1]
output_sra = sys.argv[2]
aspera_key = sys.argv[3]

# Read input list
with open(input_list, 'r') as g:
    files = [line.strip() for line in g.readlines()]

random.shuffle(files)
# For each id in input download sra file
for f in files:
    print("Downloading:", f, file=sys.stderr)
    url = "anonftp@130.14.250.7:/sra/sra-instant/reads/ByRun/sra/%s/%s/%s/%s.sra" % (f[:3], f[:6], f, f)
    filename = f + '.sra'
    if not os.path.exists(os.path.join(output_sra, filename)):
        print(url, file=sys.stderr)
        subprocess.call(["ascp", "-T", "-Q", "-l100m", "-i", aspera_key, url, output_sra])
    else:
        print(".sra file found, skipping")
