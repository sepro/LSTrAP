import argparse
import sys
from collections import defaultdict

import networkx as nx
import matplotlib.pyplot as plt

DEBUG = True


def plot_network(filename, gene, cutoff=0.7):
    """
    Function to load a co-expression network from LSTrAP and plot the neighborhood for one gene.

    :param filename: PCC output to load
    :param gene: The gene whose neighborhood to visualize
    :param cutoff: PCC cutoff to use, default 0.7
    """
    print("Loading file %s ..." % filename, end='')

    network_full = defaultdict(dict)
    query = None # this will store the query gene with the right case once found

    with open(filename, "r") as fin:
        for i, line in enumerate(fin, start=1):
            try:
                g, network = line.strip().split(':')

                targets = network.strip().split()

                target_list = {}
                found_query = False
                if g.lower() == gene.lower():
                    found_query = True
                    query = g

                for t in targets:
                    target, score = t.strip(')').split('(')
                    score = float(score)

                    if score >= cutoff:
                        target_list[target] = score

                        if target.lower() == gene.lower():
                            found_query = True

                if found_query:
                    network_full[g] = target_list

            except Exception as e:
                print("\nAn error occurred while reading line %d!" % i, file=sys.stderr)
                print(line, file=sys.stderr)

    print("Done!")
    print("Plotting graph for %s with PCC cutoff of %.2f" % (query, cutoff))

    if DEBUG:
        print(network_full[query])
        print(type(network_full[query]))

    valid_genes = [query]

    for k, _ in network_full[query].items():
        valid_genes.append(k)

    if DEBUG:
        print(valid_genes)

    graph = nx.Graph()
    graph.add_nodes_from(valid_genes)

    for g, targets in network_full.items():
        for target, score in targets.items():
            if g in valid_genes and target in valid_genes:
                graph.add_edge(g, target, weight=score)

    # plot graph

    pos = nx.spring_layout(graph)

    nx.draw_networkx_nodes(graph, pos,
                           node_color='#42bcf4',
                           node_size=500,
                           alpha=0.8)

    nx.draw_networkx_edges(graph, pos,
                           width=3, alpha=0.5, edge_color='0.5')

    nx.draw_networkx_labels(graph, pos, {k: k for k in valid_genes}, font_size=16, alpha=0.5)

    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="./plot_network.py")

    parser.add_argument('filename', help='PCC output from LSTrAP')
    parser.add_argument('gene', help='Gene for which the networks will be drawn')

    parser.add_argument('--cutoff', help='PCC cutoff to use (default = 0.7)', default=0.7, type=float)

    parser.set_defaults(show_labels=True)

    # Parse arguments and start script
    args = parser.parse_args()

    plot_network(args.filename, args.gene, cutoff=args.cutoff)

