import os
import shutil
import gzip
import csv


def unzip_patient_data(directory):
    """
    Unzips a patient data. Removes zip files after unzipping.
    :param directory: Directory of patient data.
    """
    extension = ".gz"
    os.chdir(directory)
    current_directory = os.getcwd()
    for folder in os.listdir(current_directory):
        if folder == "MANIFEST.txt":
            os.remove(folder)
        else:
            for file in os.listdir(folder):
                if file.endswith(extension):
                    gz_name = os.path.abspath(file)
                    file_name = (os.path.basename(gz_name)).rsplit('.', 1)[0]
                    absolute_path = "{}\{}\{}".format(current_directory, folder, file)
                    extract_to = "{}\{}".format(folder, file_name)
                    with gzip.open(absolute_path, "rb") as f_in, open(extract_to, "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)
                    if file != file.endswith('.htseq_counts.txt'):
                        os.remove(file)
                    os.remove(absolute_path)
    os.chdir("../..")


def unzip(directory):
    """
    Unzips .tar.gz files.
    :param directory: Directory of .tar.gz file.
    """
    extension = ".tar.gz"
    extract_dir = 'cases'
    os.chdir(directory)
    current_directory = os.getcwd()
    for file in os.listdir(current_directory):
        if file.endswith(extension):
            gz_name = os.path.abspath(file)
            shutil.unpack_archive(gz_name, extract_dir)
            os.remove(gz_name)
    os.chdir("..")


def parse_sample_sheet(directory):
    """
    Reads the sample sheet and returns a dictionary of case id, lung type and file id.
    :param directory: Directory of the sample sheet.
    :return: Dictionary of the parse sheet.
    """
    extension = ".tsv"
    os.chdir(directory)
    current_directory = os.getcwd()
    for file in os.listdir(current_directory):
        if file.endswith(extension):
            with open(file, 'r') as f:
                d = {}
                reader = csv.reader(f, delimiter='\t')
                next(f)
                for row in reader:
                    case_id = row[5].split(',')[0]
                    lung_type = row[7].split(',')[0]
                    file_id = "{}_{}".format(row[0], lung_type.replace(" ", "_"))
                    if case_id in d.keys():
                        d[case_id].append({file_id: []})
                    else:
                        d.update({case_id: [{file_id: []}]})
    os.chdir("..")
    return d
