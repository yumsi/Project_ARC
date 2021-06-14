"""
This script has been written to read TCGA RNA seq data.
It extracts tar.gz files, filters on ribosomal genes and saves this in a JSON format.
It can also normalize data if needed.

@Author:    Lars Maas
@Date:      7-06-2021
@Version:   1.0
"""
import copy
import csv
import json
import os
import tarfile
import gzip
import glob


def extract_tar(path):
    """
    Extract tar.gz folder
    :param path: String containing the folder from a cancer type.
    """
    tar_file = ''
    for filename in os.listdir(f'Data/{path}/input'):
        if filename.endswith('.tar.gz'):
            tar_file = filename

    if tar_file == '':
        exit(f'No tar.gz file found in: {path}/input. '
             f'Please put this file in the "input" directory and/or set the PATH variable right.')
    with tarfile.open(f'Data/{path}/input/{tar_file}', 'r:gz') as tar:
        tar.extractall(f'Data/{path}/cases_extracted')


def readtsv(path):
    """
    give a gdc sample sheet (tsv)
    :param path: String containing the folder from a cancer type.
    :return: Dictionary containing patient id's as keys and None type as value.
    """
    sample_sheet = ''
    for filename in os.listdir(f'Data/{path}/input'):
        if filename.endswith('.tsv'):
            sample_sheet = filename
    if sample_sheet == '':
        exit(f'No gdc sample sheet tsv file found in: Data/{path}/input. '
             f'Please put this file in the "input" directory and/or set the PATH variable right.')

    with open(f'Data/{path}/input/{sample_sheet}', 'r') as file:
        case_info = csv.reader(file, delimiter='\t')
        next(case_info)
        case_dict = {}
        for line in case_info:
            case_id = line[5].split(',')[0]
            if case_dict.get(case_id) is None:
                case_dict[case_id] = dict()
            case_dict[case_id][f'{line[7].split(",")[0]}_{line[0]}'] = None
    return case_dict


def read_htseq(path, cases, normalize=False):
    """
    Reads the extracted files containing the RNA seq data. Filters, (normalizes) and puts them in the cases dictionary.
    :param path: String containing the folder from a cancer type.
    :param cases: Dictionary containing patient id's as keys and None type as value.
    :param normalize: Boolean. data will be normalized if True.
    :return: The cases dictionary, but filled with read data.
    """
    # make empty dictionary containing all ribosomal genes
    ribo_dict_empty = make_ribo_dict()

    # get all directories (* = something).
    for folder in glob.glob(f'Data/{path}/cases_extracted/*/'):
        # get first file in the directory
        gz_file = os.listdir(folder)
        if gz_file[0].endswith('.gz'):
            gz_file = gz_file[0]
        else:
            gz_file = gz_file[1]
        file_id = folder.split('/')[-2]

        # Make a copy of the empty ribosome dictionary
        ribo_dict = copy.deepcopy(ribo_dict_empty)
        # print(f'{folder}{gz_file}')
        if normalize:
            # count the total expression
            with gzip.open(f'{folder}{gz_file}', 'rt') as ht_seq:
                total_expression = 0
                for line in ht_seq:
                    line = line.strip().split('\t')
                    if not line[0].startswith('__'):
                        total_expression += int(line[1])
            # 100 chosen so the total normalized expression will be 100
            rate = 100 / total_expression

        with gzip.open(f'{folder}{gz_file}', 'rt') as ht_seq:
            for line in ht_seq:
                line = line.strip().split('\t')
                line[0] = line[0].split('.')[0]
                # Add to dictionary if gene in dictionary
                if ribo_dict.get(line[0]) is not None:
                    exp = int(line[1])
                    if normalize:
                        exp *= rate
                    ribo_dict[line[0]][3] = exp

        # Delete all dictionary entries from which no count data is available
        ensg_not_found = []
        for ensg, value in ribo_dict.items():
            if value[3] == -1:
                ensg_not_found.append(ensg)

        for ensg in ensg_not_found:
            del ribo_dict[ensg]

        # Add filled gene count dictionary to cases dictionary
        for case, file_ids in cases.items():
            for case_file_id in file_ids.keys():
                if case_file_id.split('_')[1] == file_id:
                    cases[case][case_file_id] = ribo_dict
                    break
    return cases


def make_ribo_dict():
    """
    Makes a dictionary containing all ribosomal genes.
    :return: Dictionary containing all ribosomal genes.
    """
    rib_genes = {}
    try:
        with open('Data/all_rp_genes.csv') as file:
            ribo_info = csv.reader(file, delimiter=',')
            next(ribo_info)
            for row in ribo_info:
                for ensg in row[2].split('; '):
                    rib_genes[ensg] = [row[0], row[1], row[3], -1]
        return rib_genes
    except FileNotFoundError:
        exit('File Data/all_rp_genes.csv not found.')


def save_ribo_expression(all_info, path, normalized):
    """
    Saves the ribosomal expression in JSON format.
    :param all_info: Dictionary with case id as key and count data as value
    :param path: String containing the folder from a cancer type.
    :param normalized: Boolean. Name of file saved depends this value.
    :return:
    """
    if normalized:
        with open(f'Data/{path}/output/ribo_gene_counts_normalized_all.json', 'w') as file:
            json.dump(all_info, file, indent=4)
        print(f'Data/{path}/output/ribo_gene_counts_normalized_all.json')
    else:
        with open(f'Data/{path}/output/ribo_gene_counts_not_normalized.json', 'w') as file:
            json.dump(all_info, file, indent=4)


def main(PATH):
    """
    Calls all other functions
    :param PATH: String containing the folder from a cancer type.
    """
    extract_tar(PATH)
    # not normalized
    allinfo = read_htseq(PATH, readtsv(PATH), normalize=False)
    save_ribo_expression(allinfo, PATH, False)

    # normalized
    allinfo = read_htseq(PATH, readtsv(PATH), normalize=True)
    save_ribo_expression(allinfo, PATH, True)


if __name__ == '__main__':
    main(PATH='Data/lung_cancer_all')

# JSON format:
# {
# case_id1: {
#   file_id1: {
#       ensg: [protein_id, hgnc symbol, count]}}
