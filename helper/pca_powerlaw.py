""""
centers and scales the data from expression matrix and then plots the PCA result
input: expression matrix, file with RunIDs, SRAIDs and description eg. tissues
output: plot with the points colored by the tissues that were taken for the given experiment

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA as sklearnPCA
from sklearn import preprocessing
import seaborn as sns

import argparse

from parsers import read_annotation


def run_pca(expression, annotation, powerlaw):
    tissue_data, description_data = read_annotation(annotation)

    # Load Expression data
    df = pd.read_table(expression, header=0, index_col=0)
    run_ids = list(df.columns.values)
    dataMatrix = np.transpose(np.array(df))

    # Run PCA
    sklearn_pca = sklearnPCA(n_components=2)
    sklearn_transf = sklearn_pca.fit_transform(preprocessing.maxabs_scale(dataMatrix, axis=0))

    # Tissues and color table
    tissues = [tissue_data[r.replace('.htseq', '')] for r in run_ids]
    colors = {'leaf': 'green', 'root': 'brown', 'shoot': 'blue', 'plant': 'black', 'seed': 'red', 'flower': 'cyan', 'stem': 'yellow', 'seedling': 'white', 'pollen': 'violet'}

    found_tissues = {}

    plt.figure(1)

    with sns.axes_style("whitegrid", {"grid.linestyle": None}):
        plt.subplot(121)
        for run, tissue, pca_data in zip(run_ids, tissues, sklearn_transf):
            label = tissue if tissue in colors.keys() else 'other'

            plt.plot(pca_data[0], pca_data[1], 'o',
                     markersize=7,
                     color=colors[tissue] if tissue in colors.keys() else 'gray',
                     alpha=0.5,
                     label=label if label not in found_tissues.keys() else "_nolegend_")

            found_tissues[label] = True

        plt.xlabel('PC 1 (%0.2f %%)' % (sklearn_pca.explained_variance_ratio_[0]*100))
        plt.ylabel('PC 2 (%0.2f %%)' % (sklearn_pca.explained_variance_ratio_[1]*100))

        plt.legend()
        plt.draw()

    with sns.axes_style("whitegrid"):
        plt.subplot(122)

        df = pd.read_table(powerlaw, names=['Node degree', 'Gene count'])

        ax = sns.regplot(x='Node degree', y='Gene count', data=df, fit_reg=False)
        ax.set(xlim=(1, 10000), ylim=(1, 10000), xscale='log', yscale='log')

    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="./pca_powerlaw.py")

    parser.add_argument('expression', help='path to expression matrix')
    parser.add_argument('annotation', help='path to sample annotation')
    parser.add_argument('powerlaw', help='path to node degree distribution')

    # Parse arguments and start script
    args = parser.parse_args()

    run_pca(args.expression, args.annotation, args.powerlaw)