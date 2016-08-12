#!/usr/bin/env python3
"""
Script to iterate over TopHat output and grab quality statistics
"""
import os
import re

from sys import argv
from collections import defaultdict

tophat_path = argv[1]

values = defaultdict(list)

# Prepare regex
re_mapped = re.compile('Mapped   :.*\(\s*(.*)% of input\)')

# Get all directories in this path
for d in os.listdir(path=tophat_path):

    # Only consider directories
    if os.path.isdir(os.path.join(tophat_path, d)):
        summary = os.path.join(tophat_path, d, 'align_summary.txt')

        # Check if summary exists
        if os.path.exists(summary):
            # process summary file
            with open(summary) as f:
                lines = '\t'.join(f.readlines())
                hits = re_mapped.search(lines)
                if hits:
                    values['samples'].append(d)
                    values['mapped_percentages'].append(float(hits.group(1)))

print('sample', 'mapped_percentage', sep='\t')
for s, p in zip(values['samples'], values['mapped_percentages']):
    print(s, p, sep='\t')