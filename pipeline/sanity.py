import configparser

import sys

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
                pass
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