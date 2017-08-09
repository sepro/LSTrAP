import argparse
import sys

import pandas as pd


def merge_matrix(first, second, output):
    """
    This function will take two matrices and merge them

    :param first:   first input matrix (path)
    :param second:  second input matrix (path)
    :param output:  output matrix (path)
    """

    df_first = pd.read_table(first, header=0, index_col=0)
    df_second = pd.read_table(second, header=0, index_col=0)

    if df_first.shape[0] != df_second.shape[0]:
        print("WARNING: attempting to merge two matrices with a different number of rows", file=sys.stderr)

    df_output = pd.concat([df_first, df_second], axis=1)

    if any([df_first.shape[0] != df_output.shape[0],
           df_second.shape[0] != df_output.shape[0],
           df_output.shape[1] != df_first.shape[1] + df_second.shape[1]]):
        print("WARNING: output matrix has an unexpected shaped", file=sys.stderr)

    df_output.index.name = 'gene'
    df_output.to_csv(output, sep='\t')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="./merge_matrix.py")

    parser.add_argument('first',  help='first LSTrAP matrix to merge')
    parser.add_argument('second', help='second LSTrAP matrix to merge')
    parser.add_argument('output', help='path to output')

    args = parser.parse_args()

    merge_matrix(args.first, args.second, args.output)
