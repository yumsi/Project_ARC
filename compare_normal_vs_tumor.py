"""
@version: 1.1.0 (14-06-2021)

@author: Julian Lerrick

Compares count data based on (a) gene name(s) between normal solid tissue and primary tumor.

"""

import json
import os


def compare(gene_name):
    """
    Compares the difference in count data of a single gene between "normal solid tissue" and "primary tumor".
    :param gene_name: Name of the gene.
    """
    count_tumor = []
    count_normal = []
    file_name = 'combined_data_normalized.json'
    path = 'data/output'
    file_path = os.path.join(path, file_name)
    f = open(file_path)
    d = json.load(f)
    for keys in d:
        for idx, k in enumerate(d[keys]):
            for key in k:
                for count in d[keys][idx][key]:
                    if count['gene'] == gene_name and key.endswith('_Primary_Tumor'):
                        count_tumor.append(count['count'])
                    elif count['gene'] == gene_name and key.endswith('_Solid_Tissue_Normal'):
                        count_normal.append(count['count'])
    calc_comparison(count_tumor, count_normal)


def calc_comparison(list_tumor, list_normal):
    """
    Calculates the difference based on count data within "normal solid tissue" and "primary tumor".
    :param list_tumor: List of count data from a gene in "primary tumor".
    :param list_normal:List of count data from a gene in "normal solid tissue".
    """
    higher = []
    lower = []
    for x in zip(list_tumor, list_normal):
        if x[0] > x[1]:
            higher.append("true")
        elif x[0] < x[1]:
            lower.append("true")
    total_length = len(lower) + len(higher)
    print("Tumor: ")
    print(len(higher))
    print("Normal: ")
    print(len(lower))
    calc_difference = len(higher) / total_length
    print("Percentage of total: " + str(calc_difference))


def compare_two_genes(gene_of_interest, gene_name):
    """
    Compares the difference in count data of two genes between "normal solid tissue" and "primary tumor".
    :param gene_of_interest: Gene name of interest.
    :param gene_name: Second gene name.
    """
    count_interest_tumor = []
    count_tumor = []
    count_interest_normal = []
    count_normal = []
    file_name = 'combined_data_normalized.json'
    path = 'data/output'
    file_path = os.path.join(path, file_name)
    f = open(file_path)
    d = json.load(f)
    for keys in d:
        for idx, k in enumerate(d[keys]):
            for key in k:
                for count in d[keys][idx][key]:
                    if count['gene'] == gene_name and key.endswith('_Primary_Tumor'):
                        count_tumor.append(count['count'])
                    elif count['gene'] == gene_of_interest and key.endswith('_Primary_Tumor'):
                        count_interest_tumor.append(count['count'])
                    elif count['gene'] == gene_of_interest and key.endswith('_Solid_Tissue_Normal'):
                        count_interest_normal.append(count['count'])
                    elif count['gene'] == gene_name and key.endswith('_Solid_Tissue_Normal'):
                        count_normal.append(count['count'])
    calc_comparison_two_genes(count_interest_tumor, count_tumor, count_interest_normal, count_normal)


def calc_comparison_two_genes(list_interest_tumor, list_tumor, list_interest_normal, list_normal):
    """
    Calculates the difference based on count data within "normal solid tissue" and "primary tumor".
    :param list_interest_tumor: Count data of gene of interest in the "primary tumor".
    :param list_tumor:Count data of the second gene in the "primary tumor".
    :param list_interest_normal: Count data of gene of interest in the "normal solid tissue".
    :param list_normal: Count data of the second gene in the "normal solid tissue".
    """
    higher = []
    lower = []
    interest_higher = []
    interest_lower = []
    for x in zip(list_interest_tumor, list_tumor, list_interest_normal, list_normal):
        if (x[1] > x[3]) and (x[0] > x[2]):
            higher.append("true")
        elif (x[1] < x[3]) and (x[0] < x[2]):
            lower.append("true")
        elif (x[1] > x[3]) and (x[0] < x[2]):
            interest_higher.append("true")
        elif (x[1] < x[3]) and (x[0] > x[2]):
            interest_lower.append("true")

    total_length = len(list_tumor)
    print("Total of amount: ")
    print(total_length)
    print("Both are higher in tumor: ")
    print(len(higher))
    print("Both are lower in tumor: ")
    print(len(lower))
    print("Interest higher in tumor - compare gene lower: ")
    print(len(interest_higher))
    print("Interest lower in tumor - compare gene higher: ")
    print(len(interest_lower))
    calc_difference = (len(higher) + len(lower)) / total_length
    print("Percentage of total: " + str(calc_difference) + " " + str(len(higher) + len(lower)) +
    "/" + str(total_length))


if __name__ == "__main__":
    gene_name_input = input("Enter gene name: ")
    compare(gene_name_input)

    # gene_of_interest = input("Enter gene of interest: ")
    # compare_with = input("Enter gene to compare with: ")
    # compare_two_genes(gene_of_interest, compare_with)
    # list_of_interest = ['RIOX2', 'RPL8', 'RPL27A', 'RPLP0', 'RPS23']
    # for x in list_of_interest:
    #     compare(x)
