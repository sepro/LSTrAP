from collections import defaultdict


def read_annotation(filename):
    tissue_data = {}
    description_data = {}

    with open(filename, 'r') as f:
        for line in f:
            columns = line.strip().split('\t')
            sra_id = columns[0]
            replicate = columns[2]
            description = columns[3]
            tissue = columns[4]
            condition = columns[5]
            stage = columns[6]
            run_id = columns[7]

            tissue_data[run_id] = tissue.strip()
            description_data[run_id] = description.strip()

    return tissue_data, description_data


def read_single_copy(filename, selected_species='sbi.fasta'):
    single_copy_genes = []

    with open(filename, 'r') as f:
        for line in f:
            _, species, gene = line.strip().split('\t')

            if species == selected_species:
                single_copy_genes.append(gene)

    return single_copy_genes


def read_single_copy_dict(filename):
    single_copy_genes = defaultdict(dict)

    with open(filename, 'r') as f:
        for line in f:
            og, species, gene = line.strip().split('\t')

            single_copy_genes[species][gene] = og

    return single_copy_genes
