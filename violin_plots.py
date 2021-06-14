"""
This script has been written to make and save violin plots of ribosomal expression data.

@Author:    Lars Maas
@Date:      7-06-2021
@Version:   1.0
"""
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
import json
import math
import Normalize_ribosomes


def read_json(PATH, normal):
    """
    Reads the JSON file containing the expression data and returns a dictionary.
    :param PATH: String containing the folder from a cancer type.
    :param normal: Opens different file based on this Boolean.
    :return: Dictionary containing expression data.
    """
    if not normal:
        with open(f'Data/{PATH}/output/ribo_gene_counts_not_normalized.json') as file:
            return json.load(file)
    with open(f'Data/{PATH}/output/ribo_gene_counts_normalized_all.json') as file:
        return json.load(file)


def get_totals(data):
    """
    Calculates the total normal and tumor expression.
    :param data: Dictionary containing expression data from 1 case.
    :return: the total normal and tumor expression data.
    """
    normal = []
    tumor = []
    for case_id, case_data in data.items():
        for reads, ensgs in case_data.items():
            if 'Tumor' in reads:
                tum = True
            else:
                tum = False
            read_count = 0
            for ensg, gene_inf in ensgs.items():
                read_count += gene_inf[3]
            tumor.append(read_count) if tum else normal.append(read_count)
    return normal, tumor


def bell_curve(totals, names):
    for total, name in zip(totals, names):
        total.sort()
        mean = np.mean(total)
        std = np.std(total)
        pdf = norm.pdf(total, mean, std)
        plt.plot(total, pdf, label=name)
    plt.title('normal distribution of all ribosmal gene expression')
    plt.xlabel('Expression count')
    plt.ylabel('sum of reads with similar expression')
    plt.legend(loc='upper right')
    plt.show()


def get_proteins(data):
    """
    Extracts the normal and tumor expression counts for each gene and puts them in a list.
    :param data: Dictionary containing expression data from all cases.
    :return: Dictionary with gene names as key and lists containing expression data as value.
    """
    proteins = {}

    for case_id, case_data in data.items():
        for reads, ensgs in case_data.items():
            for ensg, gene_inf in ensgs.items():
                proteins[gene_inf[0]] = {'normal': [], 'tumor': []}
            break
        break

    for case_id, case_data in data.items():
        for reads, ensgs in case_data.items():
            # tum = True if 'Tumor' in reads else False
            if 'Tumor' in reads:
                tum = True
            else:
                tum = False
            for ensg, gene_inf in ensgs.items():
                if tum:
                    proteins[gene_inf[0]]['tumor'].append(gene_inf[3])
                else:
                    proteins[gene_inf[0]]['normal'].append(gene_inf[3])
    return proteins


def adjacent_values(vals, q1, q3):
    """
    Calculates the size of the whiskers of the violin plot.
    :param vals: List containing all expression data.
    :param q1: 1st quartile distance.
    :param q3: 3rd quartile distance.
    :return: The upper and lower value of the violin plot whisker.
    """
    upper_adjacent_value = q3 + (q3 - q1) * 1.5
    upper_adjacent_value = np.clip(upper_adjacent_value, q3, vals[-1])

    lower_adjacent_value = q1 - (q3 - q1) * 1.5
    lower_adjacent_value = np.clip(lower_adjacent_value, vals[0], q1)
    return lower_adjacent_value, upper_adjacent_value


def violin_plot(proteins, PATH, norm):
    """
    Creates and saves violin plots.
    :param proteins: Dictionary containing expression data from all cases.
    :param PATH: String containing the folder from a cancer type.
    :param norm: String. Can contain 'ribo', 'no' or 'all'. Based on this. A different Y axes value
    and file name are chosen.
    """
    # Determine what size the figure has to be and the number of rows and number of columns needed.
    n = math.ceil(math.sqrt(len(proteins)))  # n * n == slightly more than number of proteins
    col = 0
    row = 0
    # Make a figure with a grid containing plots
    fig, axs = plt.subplots(nrows=n, ncols=n, figsize=(20 + n, 20 + n))

    for prot, reads in proteins.items():
        # Sort the reads
        normal = sorted(reads['normal'])
        tumor = sorted(reads['tumor'])
        # Determine the plot to be used for the protein
        if col == n:
            col = 0
            row += 1
        ax = axs[row, col]
        # Set plot options
        ax.set_title(f'violin plot of {prot}')
        if norm == 'no':
            ax.set_ylabel('Gene expression')
        elif norm == 'ribo':
            ax.set_ylabel('% of total ribosomal expression')
        elif norm == 'all':
            ax.set_ylabel('% of total expression')
        else:
            exit('no normalization function')

        ax.set_xlabel('Sample')
        # Make violin plots
        parts = ax.violinplot([normal, tumor], showmeans=True, showmedians=False, showextrema=False)
        for pc in parts['bodies']:
            # pc.set_facecolor('red')
            pc.set_edgecolor('black')
            pc.set_alpha(0.5)
        # parts['bodies'][0].set_facecolor('red')
        # parts['bodies'][1].set_alpha(1)

        # Determine 1qst quartile, median and 3rd quartile
        quartile1, medians, quartile3 = np.percentile([normal, tumor], [25, 50, 75], axis=1)
        # Calculate whiskers to be used
        whiskers = np.array([adjacent_values(sorted_array, q1, q3) for sorted_array, q1, q3 in zip([normal, tumor], quartile1, quartile3)])
        whiskers_min, whiskers_max = whiskers[:, 0], whiskers[:, 1]

        inds = np.arange(1, len(medians) + 1)
        # Add whiskers, 1st quartile, median en 3rd quartile
        ax.scatter(inds, medians, marker='o', color='white', s=10, zorder=3)
        ax.vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=5)
        ax.vlines(inds, whiskers_min, whiskers_max, color='k', linestyle='-', lw=1)

        # ax.xaxis.set_tick_params(direction='out')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_xticks(np.arange(1, 2 + 1))
        ax.set_xticklabels(['normal', 'tumor'])
        # ax.set_xlim(0.25, 2 + 0.75)
        col += 1

    fig.tight_layout()
    if norm == 'no':
        plt.savefig(f'Data/{PATH}/output/violinplot_not_normalized.png')
    elif norm == 'ribo':
        plt.savefig(f'Data/{PATH}/output/violinplot_normalized_ribos.png')
    elif norm == 'all':
        plt.savefig(f'Data/{PATH}/output/violinplot_normalized_all.png')
    # fig.show()


def main(PATH):
    """
    Calls the other functions.
    :param PATH: String containing the folder from a cancer type.
    """

    # not normalized
    # read the data
    data = read_json(PATH, normal=False)

    proteins = get_proteins(data)

    # make violin plot
    violin_plot(proteins, PATH=PATH, norm='no')

    # normalized on ribos
    # Normalize on ribo genes
    data = Normalize_ribosomes.normalize(data, path=PATH)

    proteins = get_proteins(data)

    violin_plot(proteins, PATH=PATH, norm='ribo')

    # normalized on all
    data = read_json(PATH, normal=True)

    # get normal/tumor counts for every protein {RPL4: {normal: [2, 3, 49, ...], tumor: [29, 1, 300, ...]}, RPS15: ...}
    proteins = get_proteins(data)

    # make violin plot
    violin_plot(proteins, PATH=PATH, norm='all')


if __name__ == '__main__':
    main(PATH='Data/lung_cancer_all')
