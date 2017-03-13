import argparse
import sys
import json

LOCUS_FEATURES = ['gene']
TRANSCRIPT_FEATURES = ['mRNA', 'transcript']
PARTS_FEATURES = ['exon', 'CDS', 'three_prime_UTR', 'five_prime_UTR']

COLUMNS = ['chr', 'source', 'feature', 'start', 'stop', 'score', 'strand', 'phase', 'attributes']

ID_ATTRIBUTE = 'ID'
PARENT_ATTRIBUTE = 'Parent'


def parse_attributes(attribute_str):
    attributes = attribute_str.split(';')
    output = {}

    for attribute in attributes:
        key, value = attribute.split('=')
        output[key] = value

    return output


def parse_line(line):
    parts = line.strip().split('\t')

    output = {}

    if len(parts) != len(COLUMNS):
        raise Exception('Incorrect number of columns in line.', parts, COLUMNS)

    for key, value in zip(COLUMNS, parts):
        if key == 'attributes':
            output[key] = parse_attributes(value)
        elif key == 'start' or key == 'stop':
            output[key] = int(value)
        else:
            output[key] = value

    return output


def parse_gff3(filename):
    genes = {}
    transcript_to_locus = {}

    with open(filename) as gff_in:
        for line in gff_in:
            # Skip comments
            if not line.strip()[0] == '#':
                line_data = parse_line(line)

                # Every line needs a valid ID
                if ID_ATTRIBUTE in line_data['attributes'].keys():

                    if line_data['feature'] in LOCUS_FEATURES:
                        genes[line_data['attributes'][ID_ATTRIBUTE]] = {
                            'data': line_data,
                            'transcripts': {}
                        }

                    elif line_data['feature'] in TRANSCRIPT_FEATURES:
                        if PARENT_ATTRIBUTE in line_data['attributes'].keys():
                            parent_id = line_data['attributes'][PARENT_ATTRIBUTE]

                            if parent_id in genes.keys():
                                genes[parent_id]['transcripts'][line_data['attributes'][ID_ATTRIBUTE]] = {
                                        'data': line_data,
                                        'parts': []
                                    }

                                transcript_to_locus[line_data['attributes'][ID_ATTRIBUTE]] = \
                                    line_data['attributes'][PARENT_ATTRIBUTE]

                    elif line_data['feature'] in PARTS_FEATURES:

                        if PARENT_ATTRIBUTE in line_data['attributes'].keys():
                            parent_id = line_data['attributes'][PARENT_ATTRIBUTE]
                            grandparent_id = transcript_to_locus[parent_id]

                            genes[grandparent_id]['transcripts'][parent_id]['parts'].append(line_data)

    return genes


def filter_genes(genes):
    return genes


def write_gff(genes, output=sys.stdout):
    print(json.dumps(genes, sort_keys=True, indent=4, separators=(',', ': ')))

if __name__ == "__main__":
    data = parse_gff3(sys.argv[1])

    filtered_genes = filter_genes(data)

    write_gff(filtered_genes)
