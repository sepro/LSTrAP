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
            required_keys = ['cds_fasta', 'protein_fasta', 'genome_fasta', 'gff_file', 'gff_feature', 'gff_id',
                             'fastq_dir', 'bowtie_output', 'trimmomatic_output', 'tophat_output', 'samtools_output',
                             'htseq_output', 'exp_matrix_output', 'exp_matrix_tpm_output', 'exp_matrix_rpkm_output',
                             '']
            required_paths = ['cds_fasta', 'protein_fasta', 'genome_fasta', 'gff_file', 'fastq_dir']

            for g in genomes:
                if not all([i in cp[g].keys() for i in required_keys]):
                    print("Missing key in", g, file=sys.stderr)

                    for i in required_keys:
                        if i not in cp[g].keys():
                            print("\tMissing", i, file=sys.stderr)
                    return False

                if not all([os.path.exists(cp[g][f]) for f in required_paths]):
                    print("Missing file/dir for", g, file=sys.stderr)
                    for f in required_paths:
                        if not os.path.exists(cp[g][f]):
                            print(f + " doesn't point to a valid file/dir", file=sys.stderr)
                    return False
        else:
            print("genomes missing from GLOBAL section", file=sys.stderr)
            return False
    else:
        print("GLOBAL section missing", file=sys.stderr)
        return False
    return True


def check_sanity_config(filename):
    """
    Reads a config ini file and returns true if all required information is there

    :param filename: ini file to check
    :return: boolean, true if the file is correct false if not
    """
    cp = configparser.ConfigParser()
    cp.read(filename)

    required_keys = ['bowtie_module', 'samtools_module', 'sratoolkit_module', 'tophat_module', 'interproscan_module',
                     'blast_module', 'mcl_module', 'python_module', 'python3_module', 'bowtie_cmd', 'trimmomatic_se_command',
                     'trimmomatic_pe_command', 'tophat_se_cmd', 'tophat_pe_cmd', 'samtools_cmd', 'htseq_count_cmd',
                     'interproscan_cmd', 'pcc_cmd', 'mcl_cmd']

    if 'TOOLS' in cp:
        if not all(k in cp['TOOLS'].keys() for k in required_keys):
            print("Missing tool found in config file", file=sys.stderr)

            for k in required_keys:
                if k not in cp['TOOLS'].keys():
                    print("Missing", k, file=sys.stderr)
            return False
    else:
        print("Tools section missing from config file", file=sys.stderr)
        return False
    return True



