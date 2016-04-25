from .parser.fasta import Fasta


def read_matrix(filename):
    """

    :param filename: the matrix containing genes id , conditions and reads
    :return: data, conditions
    """
    data = {}
    with open(filename, "r") as f:
        header = f.readline().strip().split('\t')
        conditions = header[1:]

        for row in f:
            parts = row.strip().split('\t')
            gene_id = parts[0]
            expression_values = parts[1:]

            gene_data = {}
            for condition, read_counts in zip(conditions, expression_values):
                gene_data[condition] = read_counts

            data[gene_id] = gene_data

        return data, conditions


def write_matrix(filename, conditions, data):
    """

    :param filename: the output file
    :param conditions: exprerimental conditions
    :param data: gene id and reads
    :return: matrix
    """
    with open(filename, "w") as f_norm:
        # print(header)
        header = '\t'.join(conditions)
        print("gene\t" + header, file=f_norm)

        for gene_id in data:
            nv = []
            for condition in conditions:
                nv.append(str(data[gene_id][condition]))
            joined_values = '\t'.join(nv)
            print(gene_id + "\t" + joined_values, file=f_norm)


def normalize_matrix_counts(data, conditions):
    """

    calculates the scoring factor that is needed to claculate TPM

    :param data: data form read_matrix
    :param conditions: conditions form read_matrix
    :return: dictionary normalized_data in which gene_id is the key , values are normalized data
    """
    read_counts = {}

    for condition in conditions:
        total = 0
        for gene_id in data:
            total += int(data[gene_id][condition])

        read_counts[condition] = total

    normalized_data = {}

    for gene_id in data:
        gene_normalized_data = {}

        for condition in conditions:
            if read_counts[condition] != 0:
                gene_normalized_data[condition] = (int(data[gene_id][condition]) * 1000000)/read_counts[condition]
            else:
                print('Condition without reads', condition)
                gene_normalized_data[condition] = 0

        normalized_data[gene_id] = gene_normalized_data

    return normalized_data


def normalize_matrix_length(data, fasta_file):
    """

    Needed during calculating TPM and RPKM
    calculates the read_counts divided by the gene length

    :param data: data from read_matrix
    :param fasta_file: fasta file with genes of the analyzed genome
    :return: dictionary with the obtained values in which gene_id is the key
    """
    fasta_reader = Fasta()
    fasta_reader.readfile(fasta_file)
    fasta_lengths = {}
    length_normalized_data = {}

    for gene_id, sequence in fasta_reader.sequences.items():
        # length in kb so divided by 1000
        lenseq = len(sequence)/1000
        fasta_lengths[gene_id] = lenseq

    for gene_id in data:
        if gene_id in fasta_lengths:
            if fasta_lengths[gene_id] > 0:
                length_normalized_data[gene_id] = {}
                for condition in data[gene_id]:
                    length_normalized_data[gene_id][condition] = float(data[gene_id][condition]) / fasta_lengths[gene_id]

            else:
                print("No sequence", gene_id)
        else:
            print("No sequence", gene_id)

    return length_normalized_data
