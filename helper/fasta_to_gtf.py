from parsers.fasta import Fasta
import sys


fasta_file = sys.argv[1]

fh = Fasta()

fh.readfile(fasta_file)

for k, s in fh.sequences.items():
    print('%s\t.\tCDS\t1\t%d\t.\t.\t.\tParent=%s' % (k, len(s), k))
