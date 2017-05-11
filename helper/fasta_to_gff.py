from parsers.fasta import Fasta
import sys


fasta_file = sys.argv[1]

fasta_data = Fasta.readfile(fasta_file)

for k, s in fasta_data.sequences.items():
    print('%s\t.\tCDS\t1\t%d\t.\t.\t.\tgene_id "Parent=%s"\n' % (k, len(s), k))
