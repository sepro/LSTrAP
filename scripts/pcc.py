#!/usr/bin/env python3
import argparse

import numpy as np
import sys


def pcc(filename, output, mcl_output):
    """
    Reads an htseq-count matrix, calculated the PCC (Pearson Correlation) for all pairs. It will return a text file with
    for each sequence the top 1000 strongest correlated genes and a mcl but also genemania/cytoscape compatible file
    containing all gene pairs with a correlation of 0.7 or better.

    :param filename: path to input, a htseq-count matrix file
    :param output: Matrix output, for each gene it prints the 1000 most strongly co-expressed genes
    :param mcl_output: Mcl compatible output
    """
    # Read Matrix and store nominators and denominators
    with open(filename, 'r') as fin:
        nominators, denominators, genes = [], [], []

        header = fin.readline()
        size = len(header.strip().split('\t'))

        for line in fin:
                parts = line.rstrip().split("\t")

                if size != len(parts):
                    print("Warning! Unequal number of columns found in line:\n%s.\nExpression matrix corrupt. Aborting!\n" % line, file=sys.stderr)
                    quit()

                if len(parts) == size:
                    temp = []
                    for j in range(1, len(parts)):
                        try:
                            temp.append(float(parts[j]))
                        except ValueError:
                            print("Warning! Non-number character found in line:\n%s.\nExpression matrix corrupt. Aborting!\n" % line, file=sys.stderr)
                            quit()

                    row_values = np.array(temp)
                    nomi = row_values-(sum(row_values)/len(row_values))
                    denomi = np.sqrt(sum(nomi**2))

                    if denomi != 0.0:
                        nominators.append(nomi)
                        denominators.append(denomi)
                        genes.append(parts[0])

    nominators = np.array(nominators)
    denominators = np.array(denominators)

    # Calculate PCC and write output
    with open(output, 'w') as fout, open(mcl_output, 'w') as mcl_out:
        print("Database OK.\nCalculating Pearson Correlation Coefficient and ranks.\n")
        for i, (nom, denom, gene) in enumerate(zip(nominators, denominators, genes), start=1):
            print("Calculated PCC values for sequence:%s, %d out of %d." % (gene, i, len(nominators)))

            nominator = np.dot(nominators, nom)
            denominator = np.dot(denominators, denom)
            pcc_values = nominator/denominator

            data = [{'score': p,
                     'gene': g,
                     'string': g + '(' + str(p) + ')'} for g, p in zip(genes, pcc_values) if g != gene]

            # sort by absolute pcc value
            data.sort(key=lambda x: x['score'], reverse=True)

            # get top 1000 genes and write them
            subset = data[:1000]

            fout.writelines(gene + ": " + '\t'.join([s['string'] for s in subset]) + "\n")

            for s in subset:
                if s['score'] > 0.7:
                    print(gene, s['gene'], s['score'], sep='\t', file=mcl_out)

    print("PCCs calculated and saved as %s and %s." % (output, mcl_output), file=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="./pcc.py")

    parser.add_argument('input', help='path to input')
    parser.add_argument('output', help='path to ranked output')
    parser.add_argument('mcl_output', help='path to mcl compatible output')

    args = parser.parse_args()

    pcc(args.input, args.output, args.mcl_output)
