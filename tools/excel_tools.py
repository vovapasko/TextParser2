import os

import xlrd
from credentials import home_project_directory, res_dir, res_filename

longitude_col = 1
latitude_col = 2
altitude_col = 3
index_col = 4
name_eng_col = 6
formula_col = 8
provider_col = 9


def xls_file_extractor(filename):
    # Give the location of the file
    loc = (filename)

    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    rows_amount = sheet.nrows
    providers = []
    provider_data = []
    provider = ''
    for i in range(2, rows_amount):
        row = sheet.row_values(i)
        if row[0] != '':
            provider = row[provider_col]
            index = row[index_col]
            longitude = row[longitude_col]
            latitude = row[latitude_col]
            altitude = row[altitude_col]
            name_eng = row[name_eng_col]
            formula = row[formula_col]
            row_dict = {index: {"longitude": longitude, "latitude": latitude,
                                "altitude": altitude, "name_eng": name_eng,
                                "formula": formula}}
            provider_data.append(row_dict)
        elif row[0] == '' and len(provider_data) != 0:
            providers.append({provider: provider_data})
            provider_data = []
        if i == rows_amount - 1:
            providers.append({provider: provider_data})
    sheet.cell_value(0, 0)

    print(sheet.row_values(3))


data = xls_file_extractor(res_filename)
print()
