#!/usr/bin/env python3
"""
Script to iterate over HTSEQ_count output and grab quality statistics
"""
import os
import re

from sys import argv
from collections import defaultdict

htseq_path = argv[1]

values = defaultdict(list)

quality_fields = ['__no_feature', '__ambiguous', '__too_low_aQual', '__not_aligned', '__alignment_not_unique' ]

# Get all directories in this path
for f in os.listdir(path=htseq_path):
    if os.path.isfile(os.path.join(htseq_path, f)) and f.endswith('.htseq'):
        sample = f.replace('.htseq', '')

        with open(os.path.join(htseq_path, f)) as fin:
            mapped_reads = 0

            for line in fin:
                gene, value = line.strip().rsplit(maxsplit=1)

                if gene not in quality_fields:
                    mapped_reads += int(value)
                else:
                    values[gene].append(int(value))

            values['samples'].append(sample)
            values['mapped_reads'].append(mapped_reads)

print('sample', 'mapped_reads', 'no_feature', 'ambiguous', '% mapped', '% no_feature', '% ambiguous',  sep='\t')
for s, m, n, a in zip(values['samples'], values['mapped_reads'], values['__no_feature'], values['__ambiguous']):
    total = sum([m, n, a])
    if total > 0:
        print(s, m, n, a, m*100/total, n*100/total, a*100/total, sep='\t')
