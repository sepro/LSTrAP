import argparse
import sys
import json
from collections import OrderedDict, defaultdict

LOCUS_FEATURES = ['gene']
TRANSCRIPT_FEATURES = ['mRNA', 'transcript']
PARTS_FEATURES = ['exon', 'CDS', 'three_prime_UTR', 'five_prime_UTR']

COLUMNS = ['chr', 'source', 'feature', 'start', 'stop', 'score', 'strand', 'phase', 'attributes']

ID_ATTRIBUTE = 'ID'
PARENT_ATTRIBUTE = 'Parent'


def parse_attributes(attribute_str):
    """
    Parse attribute field of GFF3 file

    :param attribute_str: attribute field as string
    :return: dict with the values for each attribute as key
    """
    attributes = attribute_str.split(';')
    output = OrderedDict()

    for attribute in attributes:
        key, value = attribute.split('=')
        output[key] = value

    return output


def parse_line(line):
    """
    Parses a (non-comment) line of a GFF3 file. The attribute field is parsed into a dict.

    :param line: line to parse as string
    :return: dict with for each column (key) the corresponding value
    """
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
    """
    Parses a GFF3 file. Returns a dictionary with all loci.

    :param filename: path the GFF3 file to parse
    :return: dict with data
    """
    genes = OrderedDict()
    transcript_to_locus = {}

    count_per_transcript = defaultdict(lambda: 1)

    with open(filename) as gff_in:
        for line in gff_in:
            # Skip comments
            if not line.strip()[0] == '#':
                line_data = parse_line(line)

                # Parts (e.g. CDS or Exon) might not have an ID. One will be added here
                if ID_ATTRIBUTE not in line_data['attributes'].keys() and line_data['feature'] in PARTS_FEATURES:
                    if PARENT_ATTRIBUTE in line_data['attributes'].keys():
                        counter_id = line_data['attributes'][PARENT_ATTRIBUTE] + '.' + line_data['feature'] + '.'
                        new_id = counter_id + str(count_per_transcript[counter_id])
                        count_per_transcript[counter_id] += 1
                        line_data['attributes'][ID_ATTRIBUTE] = new_id

                # Every line needs a valid ID
                if ID_ATTRIBUTE in line_data['attributes'].keys():

                    if line_data['feature'] in LOCUS_FEATURES:
                        genes[line_data['attributes'][ID_ATTRIBUTE]] = {
                            'data': line_data,
                            'transcripts': OrderedDict()
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


def format_attributes(attributes):
    """
    Takes an attribute dict and converts it to string

    :param attributes: dict with attributes
    :return: string with attributes in GFF3 format
    """
    return ';'.join([k + '=' + v for k, v in attributes.items()])


def format_line(line_data):
    """
    Takes parsed GFF3 data (loci, transcripts or parts) and converts it back into a valid GFF3 Line

    :param line_data: dict with data
    :return: string in GFF3 format
    """
    output = []
    for column in COLUMNS:
        output.append(str(line_data[column]) if column != 'attributes' else format_attributes(line_data[column]))

    return '\t'.join(output)


def format_gene(gene_data):
    """
    Takes parsed GFF3 data for a gene and returns it as a formatted GFF3 string

    :param gene_data: dict with parsed data
    :return: string with GFF3 formatted data
    """
    output = [format_line(gene_data['data'])]

    for _, transcript in gene_data['transcripts'].items():
        output.append(format_line(transcript['data']))
        for part in transcript['parts']:
            output.append(format_line(part))

    return '\n'.join(output)


def filter_genes(genes, output=sys.stdout):
    """
    Select longest transcript and print output

    :param genes: parsed GFF3 data
    :param output: filehandle to write output to, default stdout
    """
    for _, gene_data in genes.items():
        new_gene = OrderedDict({'data': gene_data['data'], 'transcripts': OrderedDict()})

        sorted_transcripts = sorted(gene_data['transcripts'].values(),
                                    key=lambda x: x['data']['stop'] - x['data']['start'],
                                    reverse=True)

        longest_transcript = sorted_transcripts[0]

        new_gene['transcripts'][longest_transcript['data']['attributes']['ID']] = longest_transcript
        print(format_gene(new_gene), file=output)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="./parse_gff.py")

    parser.add_argument('filename', help='filename of GFF3 file to parse')
    parser.add_argument('--output', '-o', help='path to output, default will print to STDOUT', default=None)

    args = parser.parse_args()

    data = parse_gff3(args.filename)

    if args.output is None:
        filter_genes(data)
    else:
        with open(args.output, "w") as f_out:
            filter_genes(data, output=f_out)

