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


def run_pca(expression):
    # Load Expression data
    df = pd.read_table(expression, header=0, index_col=0)
    run_ids = list(df.columns.values)
    dataMatrix = np.transpose(np.array(df))

    run_ids = [s.split('_')[0] for s in run_ids]

    # Run PCA
    sklearn_pca = sklearnPCA(n_components=2)
    sklearn_transf = sklearn_pca.fit_transform(preprocessing.maxabs_scale(dataMatrix, axis=0))

    with sns.axes_style("whitegrid", {"grid.linestyle": None}):
        for run, pca_data in zip(run_ids, sklearn_transf):
            plt.plot(pca_data[0], pca_data[1], 'o',
                     markersize=7,
                     alpha=0.5,
                     color='gray')
            plt.text(pca_data[0], pca_data[1], run)

        plt.xlabel('PC 1 (%0.2f %%)' % (sklearn_pca.explained_variance_ratio_[0]*100))
        plt.ylabel('PC 2 (%0.2f %%)' % (sklearn_pca.explained_variance_ratio_[1]*100))

        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="./pca_plot.py")

    parser.add_argument('expression', help='path to expression matrix')

    # Parse arguments and start script
    args = parser.parse_args()

    run_pca(args.expression)