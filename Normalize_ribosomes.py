"""
Normalizes expression data based on total ribosomal expression. Saves and returns this data.
"""

import json


def normalize(proteins, path):
    """
    Normalizes expression data based on total ribosomal expression. Saves and returns this data.
    :param proteins: Dictionary containing expression data from all cases.
    :param path: String containing the folder from a cancer type.
    :return: The proteins variable but normalized.
    """
    for case_id, tissues in proteins.items():
        for tissue, ensembl in tissues.items():
            tis = 0
            for protein, count in ensembl.items():
                tis += count[3]
            exp = 100 / tis
            for protein in ensembl.keys():
                proteins[case_id][tissue][protein][3] *= exp

    with open(f'Data/{path}/output/ribo_gene_counts_normalized_ribos.json', 'w') as file:
        json.dump(proteins, file, indent=4)
    return proteins
