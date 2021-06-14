"""
Webapp that allows the visualisation of ribosomal expression data.
Author: Bram Löbker
Version: 3.0.0 (09-16-2021
"""
from flask import Flask, render_template, request
import json
from colour import Color
from flask_wtf import FlaskForm
from wtforms import SelectField

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
init = False


def read_json():
    """
    Reads JSON file with all cases from the data retrieval module and saves it in dictionary and 2D list.
    :return:cases: 2D list with lists of expression per protein
    cases_dict: Dictionary with all cases, files and expression data.
    """

    cases_dict = {}
    max_expression = 0

    with open(
            # Change Directory
            "C:\\Users\\braml\\Desktop\\Blok10\\ARC\\Updated_Visualiser\\static\\ExpressieData\\ribo_gene_counts_normalized_ribos.json") as json_file:
        data = json.load(json_file)
        cases = []
        for case in data:
            fdict = []
            for file in data[case]:
                _ = []
                for expression in data[case][file]:
                    temp = data[case][file][expression]
                    _.append([temp[0], temp[3]])
                    if int(temp[3] > max_expression):
                        max_expression = temp[3]
                files = {file: _}
                cases.append(_)
                fdict.append(files)
            cases_dict[case] = fdict

    return cases, cases_dict


# Initiates the two dropdown menus. One selects the case and then updates the one with files to show the corresponding files. (Deprecated, both files are now shown at once)
class Form(FlaskForm):
    """
    Initiates dropdown menu, used to select a specific case
    """

    cases = SelectField("case", choices=[])


cases, cases_dict = read_json()


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Functions as a main.
    :return: render_template: HTML template with all necessary information
    """

    ratiocolors = set_color_scale("blue", "red")

    colored_case, colors, bucket_ab, bucket_df, bucket_rt, bucket_abm = match_color_to_value(cases[0], 'absoluut')

    form = Form()
    form.cases.choices = [(key, key) for key in cases_dict]

    if request.method == 'POST':
        current_case = form.cases.data
        vis_choice = request.form['vistype']
        requested_dataset_c, requested_dataset_n = extract_expression_data(current_case)

    else:
        current_case = tuple(cases_dict.items())[0][0]
        vis_choice = 'ratio_C/N'
        requested_dataset_c, requested_dataset_n = extract_expression_data(current_case)

    totaal_c = 0
    for x in requested_dataset_c:
        totaal_c = totaal_c + x[1]

    totaal_n = 0
    for x in requested_dataset_n:
        totaal_n = totaal_n + x[1]

    if vis_choice == 'ratio_C/N':
        requested_dataset_r = calc_ratio(requested_dataset_c, requested_dataset_n)
        requested_dataset_d = calc_diff(requested_dataset_c, requested_dataset_n)
        data_type = "Ratio"
    if vis_choice == 'ratio_N/C':
        requested_dataset_r = calc_ratio(requested_dataset_n, requested_dataset_c)
        requested_dataset_d = calc_diff(requested_dataset_n, requested_dataset_c)
        data_type = "Ratio"

    requested_dataset_n_col = match_color_to_value(requested_dataset_n, 'absoluut')
    requested_dataset_c_col = match_color_to_value(requested_dataset_c, 'absoluut')
    requested_dataset_r = requested_dataset_r[0]
    requested_dataset_d = requested_dataset_d[0]

    return render_template("ribosoom.html", form=form, cases_n=requested_dataset_n_col[0],
                           cases_c=requested_dataset_c_col[0], cases_r=requested_dataset_r, colors=colors,
                           totaal_n=round(totaal_n), totaal_c=round(totaal_c), data_type=data_type,
                           current_case=current_case, ratiocolors=ratiocolors, bucket_ab=bucket_ab, bucket_rt=bucket_rt,
                           bucket_abm=bucket_abm, cases_d=requested_dataset_d, bucket_df=bucket_df)


def match_color_to_value(cases, datatype):
    """
    Corresponds expression value to corresponding color, as dicated by the 'buckets'
    :param cases: 2D list with lists of expression per protein
    :param datatype: 'normal', 'ratio' or 'diff'. Dictates the 'bucket' used.
    :return: colored_cases: Same as cases, but with a color hex added as 3rd index in the list
    colors: list of color hexes, used by the html page to color the scales
    buckets_ab: list of absolute 'bucket' values, used by the html page to subscript de scales
    buckets_df: list of difference 'bucket' values, used by the html page to subscript de scales
    buckets_rt: list of ratio 'bucket' values, used by the html page to subscript de scales
    buckets_abm: list of absolute mitochondria 'bucket' values, used by the html page to subscript de scales
    """

    all_buckets = []
    buckets_ab = [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 3, 4, 5, 6, 7]
    buckets_abm = [0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.5, 1, 2, 5]
    buckets_rt = [1, 1.05, 1.10, 1.15, 1.20, 1.25, 1.3, 1.35, 1.75, 2, 3, 4, 5, 7]
    buckets_df = [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 5]

    map(float, buckets_ab)
    map(float, buckets_abm)
    map(float, buckets_rt)
    map(float, buckets_df)

    if datatype == 'absoluut':
        buckets = buckets_ab
        green = Color("green")
        colors = list(green.range_to(Color("red"), 15))
        all_buckets.extend(buckets)
    elif datatype == 'ratio':
        buckets = buckets_rt
        green = Color("blue")
        colors = list(green.range_to(Color("red"), 15))
        all_buckets.extend(buckets)
    elif datatype == 'diff':
        buckets = buckets_df
        green = Color("blue")
        colors = list(green.range_to(Color("red"), 15))
        all_buckets.extend(buckets)

    colored_cases = []

    for case in cases:

        if ('MRP' in case[0] or case[0] == 'PTCD3' or case[0] == "MT-CO3" or case[0] == 'AURKAIP1' or case[0] == 'MTIF2'):

            # When a Mitochondrial protein is detected, the buckets are changed to the appropriate absolute mitochondial bucket for this specific protein. The bucket is changed back after.
            buckets = buckets_abm

            # When a Mitochondrial protein is detected and the datatype is 'ratio', the bucked is changed back to the ratio bukcet immediately. The absolute mitochondrial bucket is not needed in this case.
            if datatype == 'ratio':
                buckets = buckets_rt
                colors = set_color_scale("green", "red")
                all_buckets.extend(buckets)

            try:
                if float(case[1]) < float(buckets[0]):
                    case.append(str(colors[0]))
                if (float(case[1]) > float(buckets[0])) & (float(case[1]) < float(buckets[1])):
                    case.append(str(colors[1]))
                if (float(case[1]) > float(buckets[1])) & (float(case[1]) < float(buckets[2])):
                    case.append(str(colors[2]))
                if (float(case[1]) > float(buckets[2])) & (float(case[1]) < float(buckets[3])):
                    case.append(str(colors[3]))
                if (float(case[1]) > float(buckets[3])) & (float(case[1]) < float(buckets[4])):
                    case.append(str(colors[4]))
                if (float(case[1]) > float(buckets[4])) & (float(case[1]) < float(buckets[5])):
                    case.append(str(colors[5]))
                if (float(case[1]) > float(buckets[5])) & (float(case[1]) < float(buckets[6])):
                    case.append(str(colors[6]))
                if (float(case[1]) > float(buckets[6])) & (float(case[1]) < float(buckets[7])):
                    case.append(str(colors[7]))
                if (float(case[1]) > float(buckets[7])) & (float(case[1]) < float(buckets[8])):
                    case.append(str(colors[8]))
                if (float(case[1]) > float(buckets[8])) & (float(case[1]) < float(buckets[9])):
                    case.append(str(colors[9]))
                if (float(case[1]) > float(buckets[9])) & (float(case[1]) < float(buckets[10])):
                    case.append(str(colors[10]))
                if (float(case[1]) > float(buckets[10])) & (float(case[1]) < float(buckets[11])):
                    case.append(str(colors[11]))
                if (float(case[1]) > float(buckets[11])) & (float(case[1]) < float(buckets[12])):
                    case.append(str(colors[12]))
                if (float(case[1]) > float(buckets[12])) & (float(case[1]) < float(buckets[13])):
                    case.append(str(colors[13]))
                if float(case[1]) > float(buckets[13]):
                    case.append(str(colors[14]))
            except Exception:
                print(case[1], buckets[0])

            # The buckets are changed back here
            if datatype == 'absoluut':
                buckets = buckets_ab
                colors = set_color_scale("green", "red")
                all_buckets.extend(buckets)
            elif datatype == 'ratio':
                buckets = buckets_rt
                colors = set_color_scale("blue", "red")
                all_buckets.extend(buckets)
            elif datatype == 'diff':
                buckets = buckets_df
                colors = set_color_scale("blue", "red")
                all_buckets.extend(buckets)

        else:
            if float(case[1]) < float(buckets[0]):
                case.append(str(colors[0]))
            if (float(case[1]) > float(buckets[0])) & (float(case[1]) < float(buckets[1])):
                case.append(str(colors[1]))
            if (float(case[1]) > float(buckets[1])) & (float(case[1]) < float(buckets[2])):
                case.append(str(colors[2]))
            if (float(case[1]) > float(buckets[2])) & (float(case[1]) < float(buckets[3])):
                case.append(str(colors[3]))
            if (float(case[1]) > float(buckets[3])) & (float(case[1]) < float(buckets[4])):
                case.append(str(colors[4]))
            if (float(case[1]) > float(buckets[4])) & (float(case[1]) < float(buckets[5])):
                case.append(str(colors[5]))
            if (float(case[1]) > float(buckets[5])) & (float(case[1]) < float(buckets[6])):
                case.append(str(colors[6]))
            if (float(case[1]) > float(buckets[6])) & (float(case[1]) < float(buckets[7])):
                case.append(str(colors[7]))
            if (float(case[1]) > float(buckets[7])) & (float(case[1]) < float(buckets[8])):
                case.append(str(colors[8]))
            if (float(case[1]) > float(buckets[8])) & (float(case[1]) < float(buckets[9])):
                case.append(str(colors[9]))
            if (float(case[1]) > float(buckets[9])) & (float(case[1]) < float(buckets[10])):
                case.append(str(colors[10]))
            if (float(case[1]) > float(buckets[10])) & (float(case[1]) < float(buckets[11])):
                case.append(str(colors[11]))
            if (float(case[1]) > float(buckets[11])) & (float(case[1]) < float(buckets[12])):
                case.append(str(colors[12]))
            if (float(case[1]) > float(buckets[12])) & (float(case[1]) < float(buckets[13])):
                case.append(str(colors[13]))
            if float(case[1]) > float(buckets[13]):
                case.append(str(colors[14]))

        colored_cases.append(case)

    return colored_cases, colors, buckets_ab, buckets_df, buckets_rt, buckets_abm


def calc_ratio(requested_dataset_c, requested_dataset_n):
    """
    Calculates the ratio between the cancer and normal dataset. The order depends on which option is checked in the radio buttons in the HTML page.
    :param requested_dataset_c: 2D list, with a list per protein, containing the name, the expression value and a color hex.
    :param requested_dataset_n: 2D list, with a list per protein, containing the name, the expression value and a color hex.
    :return: colored_cases: 2D list, with a lister per protein, containing the name, the expression ratio value and a color hex.
    """

    requested_dataset_r = []

    counter = 0
    for sub in requested_dataset_n:
        try:
            if not requested_dataset_n[counter][0] == requested_dataset_c[counter][0]:
                print(requested_dataset_n[counter][0] + requested_dataset_c[counter][0])

            ratio = (float(requested_dataset_c[counter][1]) / float(requested_dataset_n[counter][1]))
        except ZeroDivisionError:
            pass
        except IndexError:
            print("Error", counter)

        requested_dataset_r.append([requested_dataset_n[counter][0], ratio])
        counter += 1

    colored_cases = match_color_to_value(requested_dataset_r, 'ratio')
    return colored_cases


def calc_diff(requested_dataset_c, requested_dataset_n):
    """
    Calculates the difference between the cancer and normal dataset. The order depends on which option is checked in the radio buttons in the HTML page.
    :param requested_dataset_c: 2D list, with a list per protein, containing the name, the expression value and a color hex.
    :param requested_dataset_n: 2D list, with a list per protein, containing the name, the expression value and a color hex.
    :return: colored_cases: 2D list, with a lister per protein, containing the name, the expression difference value and a color hex.
    """

    requested_dataset_r = []

    counter = 0
    for sub in requested_dataset_n:
        try:
            if not requested_dataset_n[counter][0] == requested_dataset_c[counter][0]:
                print(requested_dataset_n[counter][0] + requested_dataset_c[counter][0])

            difference = (float(requested_dataset_c[counter][1]) - float(requested_dataset_n[counter][1]))
        except ZeroDivisionError:
            pass
        except IndexError:
            print("Error", counter)

        requested_dataset_r.append([requested_dataset_n[counter][0], difference])
        counter += 1

    colored_cases = match_color_to_value(requested_dataset_r, 'diff')
    return colored_cases


def set_color_scale(right_col, left_col):
    """
    Initiates a list with 15 colors, ranging from right_col to left_col
    :param right_col: hex with color, will be the color the scale starts with
    :param left_col: hex with color, will be the color the scale ends with
    :return: colors: list with 15 color hexes
    """

    right_col = Color(right_col)
    colors = list(right_col.range_to(Color(left_col), 15))

    return colors


def extract_expression_data(current_case):
    """
    Extracts the expression data from the dictionairy, with the key as selected in the html page
    :param current_case: ID of case selected by the user
    :return: requested_dataset_c:  2D list, with a list per protein, containing the name and the expression value.
    requested_dataset_c:  2D list, with a list per protein, containing the name and the expression value
    """

    requested_dataset_c = []
    requested_dataset_n = []

    for x in cases_dict[current_case]:
        for key in x:
            if str(key).__contains__('Tumor'):
                requested_dataset_c = x[key]
            else:
                requested_dataset_n = x[key]

    return requested_dataset_c, requested_dataset_n


if __name__ == '__main__':
    app.run()
