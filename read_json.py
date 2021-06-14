"""
This script reads ribosomal count data and converts this to a .xlsx file.

@Author:    Lars Maas
@Date:      7-06-2021
@Version:   1.0
"""
import json
import xlsxwriter
from xlsxwriter.utility import xl_col_to_name


def main(PATH):
    """
    Calls all other functions.
    :param PATH: String containing the folder from a cancer type.
    """
    readjson(PATH, normal='no')
    readjson(PATH, normal='ribo')
    readjson(PATH, normal='all')


def add_to_sheet(work_sheet, x, y, text):
    work_sheet.write(x, y, text)


def readjson(path, normal):
    """
    Reads ribosomal count data and converts this to a .xlsx file.
    :param path: String containing the folder from a cancer type.
    :param normal: String. Can contain 'ribo', 'no' or 'all'. Based on this. A different file is chosen
    to get expression data. This also decides the name of the save file.
    """
    if normal == 'no':
        file_name = 'ribo_gene_not_normalized.xlsx'
        json_file = 'ribo_gene_counts_not_normalized.json'
    elif normal == 'ribo':
        file_name = 'ribo_gene_normalized_ribo.xlsx'
        json_file = 'ribo_gene_counts_normalized_ribos.json'
    elif normal == 'all':
        file_name = 'ribo_gene_normalized_all.xlsx'
        json_file = 'ribo_gene_counts_normalized_all.json'
    else:
        exit("No normalisation given")
    # naming the excel file and the seperate sheets
    workbook = xlsxwriter.Workbook(f'Data/{path}/output/{file_name}')
    worksheet1 = workbook.add_worksheet('ruwe data')
    worksheet2 = workbook.add_worksheet('ratio')
    worksheet3 = workbook.add_worksheet('difference')

    # Fill cells with standard names
    sheet = worksheet1
    for sheet_nr in range(3):
        if sheet_nr == 1:
            sheet = worksheet2
            add_to_sheet(worksheet2, 1, 1, 'ratio')
        elif sheet_nr == 2:
            sheet = worksheet3
            add_to_sheet(sheet, 1, 1, 'difference')
        else:
            add_to_sheet(sheet, 1, 1, 'normal')
            add_to_sheet(sheet, 1, 2, 'tumor')
        add_to_sheet(sheet, 2, 0, 'total ribosome read count')
        add_to_sheet(sheet, 3, 0, 'total cytoplastic rp count')
        add_to_sheet(sheet, 4, 0, 'cytoplastic large subunit')
        add_to_sheet(sheet, 5, 0, 'cytoplastic small subunit')
        add_to_sheet(sheet, 6, 0, 'total mitochondrial rp count')
        add_to_sheet(sheet, 7, 0, 'mitochondrial  large subunit')
        add_to_sheet(sheet, 8, 0, 'mitochondrial small subunit')
        add_to_sheet(sheet, 0, 1, 'average patient')

    column = 0
    row = 9
    try:
        with open(f'Data/{path}/output/{json_file}', 'r') as file:
            case_info = json.load(file)
    except FileNotFoundError:
        exit(f'Data/{path}/output/{json_file} not found. '
             f'Run script "count_ribosomal_expression.py" first')

    all_columns_normal = []
    all_columns_tumor = []
    for i in range(3, len(case_info) * 2 + 2, 2):
        all_columns_normal.append(xl_col_to_name(i))
        all_columns_tumor.append(xl_col_to_name(i + 1))

    # Get all ribosomal proteins
    for file_ids in case_info.values():
        for ens_ids in file_ids.values():
            for rp_data in ens_ids.values():
                worksheet1.write(row, column, f'{rp_data[0]}_{rp_data[1]}')
                worksheet2.write(row, column, f'{rp_data[0]}_{rp_data[1]}')
                worksheet3.write(row, column, f'{rp_data[0]}_{rp_data[1]}')
                row += 1
            break
        break
    column = 3
    # Add counts from total large and small subunit from cytoplasmic and mitochondrial ribosomes
    # in tumor and normal tissue
    for count, (case_id, file_ids) in enumerate(case_info.items()):
        mito_large_normal = 0
        mito_small_normal = 0
        mito_large_tumor = 0
        mito_small_tumor = 0
        cyto_large_normal = 0
        cyto_small_normal = 0
        cyto_large_tumor = 0
        cyto_small_tumor = 0
        worksheet1.write(0, column, case_id)
        worksheet1.write(1, column, 'normal')
        worksheet1.write(1, column + 1, 'tumor')

        count += 1
        worksheet2.write(0, column - count, case_id)
        worksheet2.write(1, column - count, 'ratio')

        worksheet3.write(0, column - count, case_id)
        worksheet3.write(1, column - count, 'difference')
        # Counts total reads from the large and small subunit from cytoplasmic and mitochondrial ribosomes
        # in tumor and normal tissue
        for file_id, ens_ids in file_ids.items():
            row = 9
            prot_nr = len(ens_ids)
            for ens_id, rp_data in ens_ids.items():
                if 'Normal' in file_id:
                    worksheet1.write(row, column, rp_data[3])
                    if rp_data[0].startswith('MRPL'):
                        mito_large_normal += rp_data[3]
                    elif rp_data[0].startswith('MRPS'):
                        mito_small_normal += rp_data[3]
                    elif rp_data[0].startswith('RPL'):
                        cyto_large_normal += rp_data[3]
                    elif rp_data[0].startswith('RPS'):
                        cyto_small_normal += rp_data[3]
                else:
                    worksheet1.write(row, column + 1, rp_data[3])
                    if rp_data[0].startswith('MRPL'):
                        mito_large_tumor += rp_data[3]
                    elif rp_data[0].startswith('MRPS'):
                        mito_small_tumor += rp_data[3]
                    elif rp_data[0].startswith('RPL'):
                        cyto_large_tumor += rp_data[3]
                    elif rp_data[0].startswith('RPS'):
                        cyto_small_tumor += rp_data[3]

                    worksheet2.write(row, column - count,
                                     f"='ruwe data'!{xl_col_to_name(count*2+2)}{row+1}/"
                                     f"'ruwe data'!{xl_col_to_name(count*2+1)}{row+1}")
                    worksheet3.write(row, column - count,
                                     f"='ruwe data'!{xl_col_to_name(count*2+2)}{row+1}-"
                                     f"'ruwe data'!{xl_col_to_name(count*2+1)}{row+1}")

                row += 1
        # Add calculations for ratio's and difference's in normal and tumor counts
        worksheet1.write(4, column, cyto_large_normal)
        worksheet1.write(4, column+1, cyto_large_tumor)
        worksheet2.write(4, column - count,
                         f"='ruwe data'!{xl_col_to_name(column+1)}{5}/'ruwe data'!{xl_col_to_name(column)}{5}")
        worksheet3.write(4, column - count,
                         f"='ruwe data'!{xl_col_to_name(column+1)}{5}-'ruwe data'!{xl_col_to_name(column)}{5}")

        worksheet1.write(5, column, cyto_small_normal)
        worksheet1.write(5, column + 1, cyto_small_tumor)
        worksheet2.write(5, column - count,
                         f"='ruwe data'!{xl_col_to_name(column+1)}{6}/'ruwe data'!{xl_col_to_name(column)}{6}")
        worksheet3.write(5, column - count,
                         f"='ruwe data'!{xl_col_to_name(column+1)}{6}-'ruwe data'!{xl_col_to_name(column)}{6}")
        worksheet1.write(3, column, cyto_small_normal+cyto_large_normal)
        worksheet1.write(3, column + 1, cyto_small_tumor + cyto_large_tumor)
        worksheet2.write(3, column - count,
                         f"='ruwe data'!{xl_col_to_name(column+1)}{4}/'ruwe data'!{xl_col_to_name(column)}{4}")
        worksheet3.write(3, column - count,
                         f"='ruwe data'!{xl_col_to_name(column+1)}{4}-'ruwe data'!{xl_col_to_name(column)}{4}")

        worksheet1.write(7, column, mito_large_normal)
        worksheet1.write(7, column+1, mito_large_tumor)
        worksheet2.write(7, column - count,
                         f"='ruwe data'!{xl_col_to_name(column+1)}{8}/'ruwe data'!{xl_col_to_name(column)}{8}")
        worksheet3.write(7, column - count,
                         f"='ruwe data'!{xl_col_to_name(column+1)}{8}-'ruwe data'!{xl_col_to_name(column)}{8}")
        worksheet1.write(8, column, mito_small_normal)
        worksheet1.write(8, column + 1, mito_small_tumor)
        worksheet2.write(8, column - count,
                         f"='ruwe data'!{xl_col_to_name(column+1)}{9}/'ruwe data'!{xl_col_to_name(column)}{9}")
        worksheet3.write(8, column - count,
                         f"='ruwe data'!{xl_col_to_name(column+1)}{9}-'ruwe data'!{xl_col_to_name(column)}{9}")
        worksheet1.write(6, column, mito_small_normal + mito_large_normal)
        worksheet1.write(6, column + 1, mito_small_tumor + mito_large_tumor)
        worksheet2.write(6, column - count,
                         f"='ruwe data'!{xl_col_to_name(column+1)}{7}/'ruwe data'!{xl_col_to_name(column)}{7}")
        worksheet3.write(6, column - count,
                         f"='ruwe data'!{xl_col_to_name(column+1)}{7}-'ruwe data'!{xl_col_to_name(column)}{7}")

        worksheet1.write(2, column, cyto_small_normal + cyto_large_normal + mito_large_normal + mito_small_normal)
        worksheet1.write(2, column + 1, cyto_small_tumor + cyto_large_tumor + mito_large_tumor + mito_small_tumor)
        worksheet2.write(2, column - count,
                         f"='ruwe data'!{xl_col_to_name(column+1)}{3}/'ruwe data'!{xl_col_to_name(column)}{3}")
        worksheet3.write(2, column - count,
                         f"='ruwe data'!{xl_col_to_name(column+1)}{3}-'ruwe data'!{xl_col_to_name(column)}{3}")
        # Add average for each protein
        for i in range(2, prot_nr):
            range_normal = f'{f"{i + 1},".join(all_columns_normal)}{i + 1}'
            range_tumor = f'{f"{i + 1},".join(all_columns_tumor)}{i + 1}'
            worksheet1.write(i, 1, f'=AVERAGE({range_normal})')
            worksheet1.write(i, 2, f'=AVERAGE({range_tumor})')
            worksheet2.write(i, 1, f"='ruwe data'!{xl_col_to_name(2)}{i+1}/'ruwe data'!{xl_col_to_name(1)}{i+1}")
            worksheet3.write(i, 1, f"='ruwe data'!{xl_col_to_name(2)}{i+1}-'ruwe data'!{xl_col_to_name(1)}{i+1}")

        column += 2

    workbook.close()


if __name__ == '__main__':
    main(PATH='Data/lung_cancer_all')
