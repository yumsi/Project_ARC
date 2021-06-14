"""
Calls functions from different script to extract TCGA count data, put ribosomal proteins in a JSON file,
normalise this data on total (ribosomal expression). Uses raw and normalized count data to generate Excel sheets
and violin plots.

@Author:    Lars Maas
@Date:      7-06-2021
@Version:   1.0
"""
import count_ribosomal_expression
import violin_plots
import read_json


def main():
    # This variable should contain the name of the folder (inside /Data/) you want to use during the analysis.
    folder = 'Sample_directory'

    print('Starting:\tExtracting files, normalizing on all.')
    count_ribosomal_expression.main(folder)
    print('Done:\tExtracting files, normalizing on all.')
    print("Starting:\tNormalizing on ribosome expression, Making violin plots.")
    violin_plots.main(folder)
    print("Done:\tNormalizing on ribosome expression, Making violin plots.")
    print("Starting:\tMaking excel files.")
    read_json.main(folder)
    print("Done:\tMaking excel files.")


if __name__ == '__main__':
    main()
