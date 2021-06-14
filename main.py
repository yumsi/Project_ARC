import json
import extract_files as extract
import gene_to_ensembl as convert
import os
import csv
import pandas as pd

SELECTION_PATH = 'data/gene selection'
DATA_PATH = 'data'
PATIENT_DATA_PATH = 'data/cases'
OUTPUT_DATA_PATH = 'data/output'


def main():
    """

    """
    print("Unzipping GDC download")
    extract.unzip(DATA_PATH)
    print("Unzipping cases")
    extract.unzip_patient_data(PATIENT_DATA_PATH)
    print("Parsing gdc sample sheet")
    d_sample_sheet = extract.parse_sample_sheet(DATA_PATH)

    if os.path.isfile(os.path.join(SELECTION_PATH, 'gene_list.csv')):
        combine_data(d_sample_sheet, PATIENT_DATA_PATH)
        data_normalisation(OUTPUT_DATA_PATH)
        colour_values(OUTPUT_DATA_PATH)
    else:
        print("Retrieving ensembl IDs and gene names of selected genes. This may take a few minutes.")
        convert_gene_to_ensembl(SELECTION_PATH)
        combine_data(d_sample_sheet, PATIENT_DATA_PATH)

# list_gene_names('data/gene selection/gene_list.csv')


def combine_data(dictionary, path):
    """

    :param dictionary:
    :param path:
    """
    read_d = dictionary
    for key in read_d:
        for idx, k in enumerate(read_d[key]):
            file_id = "".join(k.keys()).split("_")[0]
            if file_id in os.listdir(path):
                for keys in k:
                    print(file_id)
                    read_d[key][idx][keys] = read_expression_data(file_id, path)
    with open("data/output/combined_data_no_normalization.json", "w") as out_file:
        json.dump(read_d, out_file)


def data_normalisation(path):
    """

    :param path:
    """
    file_name = 'combined_data_no_normalization.json'
    file_path = os.path.join(path, file_name)
    f = open(file_path)
    d = json.load(f)
    for keys in d:
        for idx, k in enumerate(d[keys]):
            for key in k:
                total_count = sum_counts(d[keys][idx][key])
                rate = 100 / total_count
                for item in d[keys][idx][key]:
                    item['count'] = float(item['count']) * rate
    with open("data/output/combined_data_normalized.json", "w") as out_file:
        json.dump(d, out_file)


def sum_counts(d):
    """

    :param d:
    :return:
    """
    sum_count = sum(int(summarize['count']) for summarize in d)
    return sum_count


def read_expression_data(case, path):
    """

    :param case:
    :param path:
    :return:
    """
    combined_expression = []
    os.chdir(os.path.join(path, case))
    case_directory = os.getcwd()
    for count_data in os.listdir(case_directory):
        with open(count_data, 'r') as f, open(os.path.realpath('../../gene selection/gene_list.csv'), 'r') as f2:
            file1 = csv.DictReader(f, delimiter='\t', fieldnames=["ensembl", "count"])
            file2 = csv.DictReader(f2, delimiter='\t')
            expression_data = [row for row in file1]
            gene_list = [row for row in file2]
            for line in gene_list:
                find_in_dict = {d['ensembl'].split('.')[0]: d for d in expression_data}
                if find_in_dict[line['ensembl']]:
                    combined_expression.append({'gene': line['gene'], 'ensembl': line['ensembl'],
                                                'count': find_in_dict[line['ensembl']]['count']})
    os.chdir("../../..")
    return combined_expression


def convert_gene_to_ensembl(file):
    """

    :param file:
    """
    file = os.path.join(file, "eiwitten.txt")
    gene_ensembl_d = {}
    file = to_list(file)
    for id in file:
        ensembl = convert.convert_ID(id, 'ensembl')
        gene = convert.convert_ID(id, 'gene')
        if ensembl != '' and gene != '':
            append_value(gene_ensembl_d, 'gene', gene)
            append_value(gene_ensembl_d, 'ensembl', ensembl)
    df = pd.DataFrame.from_dict(gene_ensembl_d)
    df_rm_empty = df[df['ensembl'].str.strip().astype(bool)]
    os.chdir(SELECTION_PATH)
    df_rm_empty.to_csv("gene_list.csv", sep="\t", index=False)
    os.chdir("../..")
    print(df)


def colour_values(path):
    """

    :rtype: object
    """
    file_name = 'combined_data_normalized.json'
    file_path = os.path.join(path, file_name)
    f = open(file_path)
    d = json.load(f)
    for keys in d:
        for idx, k in enumerate(d[keys]):
            for key in k:
                gene_name = [gene['gene'] for gene in d[keys][idx][key]]
                count_to_list = [counter['count'] for counter in d[keys][idx][key]]
                max_v = max_value(count_to_list)
                min_v = min_value(count_to_list)
                for it, count in enumerate(count_to_list):
                    rgb = convert_to_rgb(min_v, max_v, count)
                    d[keys][idx][key][it] = {'gene': gene_name[it], 'colour': rgb}

    with open("data/output/color_assignment_normalized.json", "w") as out_file:
        json.dump(d, out_file)


def max_value(list_data):
    """

    :param list_data:
    :return:
    """
    max_v = max(list_data)
    return max_v


def min_value(list_data):
    """

    :param list_data:
    :return:
    """
    min_v = min(list_data)
    return min_v


def convert_to_rgb(min_value, max_value, value):
    """

    :param min_value:
    :param max_value:
    :param value:
    :return:
    """
    value = 0.67 - 0.67 * (value - min_value) / (max_value - min_value)
    R = abs(value * 6 - 3) - 1
    G = 2 - abs(value * 6 - 2)
    B = 2 - abs(value * 6 - 4)
    R = int(min(max(R, 0), 1) * 255)
    G = int(min(max(G, 0), 1) * 255)
    B = int(min(max(B, 0), 1) * 255)
    return f"#{R:02X}{G:02X}{B:02X}"


def append_value(dict_obj, key, value):
    """

    :param dict_obj:
    :param key:
    :param value:
    """
    if key in dict_obj:
        if not isinstance(dict_obj[key], list):
            dict_obj[key] = [dict_obj[key]]
        dict_obj[key].append(value)
    else:
        dict_obj[key] = value


def to_list(file):
    """

    :param file:
    :return:
    """
    with open(file) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


def list_gene_names(file):
    """

    :param file:
    """
    with open(file, 'r') as f:
        gene_names = []
        csvreader = csv.reader(f, delimiter='\t')
        fields = next(csvreader)
        for row in csvreader:
            gene_names.append(row[0])
        print(gene_names)


if __name__ == "__main__":
    main()
