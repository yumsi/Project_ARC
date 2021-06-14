import json
import os


def compare(gene_name):
    """

    :param gene_name:
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

    :param list_tumor:
    :param list_normal:
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

    :param gene_of_interest:
    :param gene_name:
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

    :param list_interest_tumor:
    :param list_tumor:
    :param list_interest_normal:
    :param list_normal:
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
