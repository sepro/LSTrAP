import pandas as pd
from scipy.spatial.distance import pdist, squareform

import seaborn as sns
import matplotlib.pyplot as plt

import argparse


def plot_data(matrix_file, show_labels=True, file_out=None, dpi_output=300, distance='euclidean'):
    df = pd.read_table(matrix_file, header=0, index_col=0)

    distances = pdist(df.values.transpose(), metric=distance)
    labels = [l.replace('.htseq', '') for l in df.columns]
    DistDf = pd.DataFrame(squareform(distances), columns=labels, index=labels)

    g = sns.clustermap(DistDf, cmap='viridis', xticklabels=show_labels, yticklabels=show_labels)
    plt.setp(g.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
    plt.setp(g.ax_heatmap.xaxis.get_majorticklabels(), rotation=90)

    if file_out is None:
        plt.show()
    else:
        plt.savefig(file_out, format='png', dpi=dpi_output)
        print("Wrote output to %s" % file_out)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="./matrix_heatmap.py")

    parser.add_argument('expression_matrix', help='path to expression matrix')
    parser.add_argument('--hide_labels', dest='show_labels', action='store_false', help='hide labels (useful for plots with many samples)')
    parser.add_argument('--png', help='save output as png file (default: None, don\'t write png to file)', default=None)
    parser.add_argument('--dpi', help='dpi for the output (default = 300)', default=300, type=float)
    parser.add_argument('--distance', help='Distance metric to use (euclidean, cityblock, ...)', default='euclidean')

    parser.set_defaults(show_labels=True)

    # Parse arguments and start script
    args = parser.parse_args()

    plot_data(args.expression_matrix,
              show_labels=args.show_labels,
              file_out=args.png,
              dpi_output=args.dpi,
              distance=args.distance)

