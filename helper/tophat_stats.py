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
re_mapped = re.compile('Mapped   :\s+\d+ \( (\d+\.*\d*) of input\)')

# Get all directories in this path
for d in os.listdir(path=tophat_path):

    # Only consider directories
    if os.path.isdir(os.path.join(tophat_path, d)):
        summary = os.path.join(tophat_path, d, 'align_summary.txt')

        # Check if summary exisists
        if os.path.exists(summary):
            # process summary file
            with open(summary) as f:
                lines = '\t'.join(f.readlines())
                print(lines)
                hits = re_mapped.search(lines)
                print(hits)
