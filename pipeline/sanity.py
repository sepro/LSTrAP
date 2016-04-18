import configparser
import sys
import os

def check_sanity_data(filename):
    """
    Reads a data ini file and returns true if all required information is there, and files/dirs exist

    :param filename: ini file to check
    :return: boolean, true if the file is correct false if not
    """
    cp = configparser.ConfigParser()
    cp.read(filename)

    if 'GLOBAL' in cp:
        if 'genomes' in cp['GLOBAL']:
            genomes = cp['GLOBAL']['genomes'].split(';')
            # For each genome test that section
            for g in genomes:

                if 'cds_fasta' not in cp[g]:
                    print(g + " missing cds_fasta", file=sys.stderr)
                    return False
                if not os.path.exists(cp[g]['cds_fasta']):
                    print(g + " cds_fasta doesn't exist", file=sys.stderr)
                    return False
                if 'genome_fasta' not in cp[g]:
                    print(g + " missing genome_fasta", file=sys.stderr)
                    return False
                if not os.path.exists(cp[g]['genome_fasta']):
                    print(g + " genome_fasta doesn't exist")
                    return False
                if 'gff_file' not in cp[g]:
                    print(g + " missing gff_file", file=sys.stderr)
                    return False
                if not os.path.exists(cp[g]['gff_file']):
                    print(g + " gff_file doesn't exist", file=sys.stderr)
                    return False
                if 'gff_feature' not in cp[g]:
                    print(g + " missing gff_feature", file=sys.stderr)
                    return False
                if 'gff_id' not in cp[g]:
                    print(g + " missing gff_id", file=sys.stderr)
                    return False
                if 'fastq_dir' not in cp[g]:
                    print(g + " missing fastq_dir", file=sys.stderr)
                    return False
                if not os.path.exists(cp[g]['fastq_dir']):
                    print(g + " fastq_dir doesn't exist", file=sys.stderr)
                    return False
                if 'bowtie_output' not in cp[g]:
                    print(g + " missig bowtie_output", file=sys.stderr)
                    return False
                if 'trimmomatic_output' not in cp[g]:
                    print(g + " missing trimmomatic_output", file=sys.stderr)
                    return False
                if 'tophat_output' not in cp[g]:
                    print(g + " missing tophat_output", file=sys.stderr)
                    return False
                if 'samtools_output' not in cp[g]:
                    print(g + " missing samtools_output", file=sys.stderr)
                    return False
                if 'htseq_output' not in cp[g]:
                    print(g + " missing htseq_output", file=sys.stderr)
                    return False

        else:
            print("genomes missing from GLOBAL section", file=sys.stderr)
            return False
    else:
        print("GLOBAL section missing", file=sys.stderr)
        return False



    return True


def check_sanity_config(filename):
    cp = configparser.ConfigParser()
    cp.read(filename)


    return True