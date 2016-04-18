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
            list_data = ['cds_fasta', 'genome_fasta', 'gff_file', 'gff_feature', 'gff_id', 'fastq_dir', 'bowtie_output', 'trimmomatic_output', 'tophat_output', 'samtools_output', 'htseq_output']
            for g in genomes:
                if not all([i in cp[g].keys() for i in list_data]):
                    print("missing data", file=sys.stderr)

                    for i in list_data:
                        if i not in cp[g].keys():
                            print("missing" + " " + i, file=sys.stderr)

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

    list_tools = ['bowtie_module', 'samtools_module', 'sratoolkit_module', 'tophat_module', 'interproscan_module', 'blast_module', 'mcl_module', 'python_module', 'bowtie_cmd', 'trimmomatic_se_command', 'trimmomatic_pe_command', 'tophat_se_cmd', 'tophat_pe_cmd', 'samtools_cmd', 'htseq_count_cmd']
    if 'TOOLS' in cp:
        if not all(k in cp['TOOLS'].keys() for k in list_tools):
            print("missing tool", file=sys.stderr)

            for k in list_tools:
                if k not in cp['TOOLS'].keys():
                    print("missing" + " " + k, file=sys.stderr)
            return False

    return True



