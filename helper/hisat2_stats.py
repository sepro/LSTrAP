#!/usr/bin/env python3
"""
Script to iterate over HISAT2 output and grab quality statistics
"""
import os
import re

from sys import argv
from collections import defaultdict

hisat2_path = argv[1]

values = defaultdict(list)

# Prepare regex
re_mapped = re.compile('\t(.*)% overall alignment rate')

# Get all directories in this path
for sf in os.listdir(path=hisat2_path):
    # Only consider .stats files
    if os.path.isfile(os.path.join(hisat2_path, sf)) and sf.endswith('.stats'):
        summary = os.path.join(hisat2_path, sf)
        # process summary file
        with open(summary) as f:
            lines = '\t'.join(f.readlines())
            hits = re_mapped.search(lines)
            if hits:
                values['samples'].append(sf)
                values['mapped_percentages'].append(float(hits.group(1)))

print('sample', 'mapped_percentage', sep='\t')
for s, p in zip(values['samples'], values['mapped_percentages']):
    print(s, p, sep='\t')
