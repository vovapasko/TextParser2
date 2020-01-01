import os
import traceback

import xlrd
import logging
from credentials import res_filename

longitude_col = 1
latitude_col = 2
altitude_col = 3
index_col = 4
name_eng_col = 6
formula_col = 8
provider_col = 9


def handle_float(number):
    try:
        float_num = float(number)
        return float_num
    except ValueError:
        try:
            new_float_num = float(number.replace(',', '.'))
            return new_float_num
        except ValueError:
            logging.error("Incorrect value in xlsx file")
            logging.error(traceback.format_exc())


def xls_file_extractor(filename):
    wb = xlrd.open_workbook(filename)
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
            longitude = handle_float(row[longitude_col])
            latitude = handle_float(row[latitude_col])
            altitude = handle_float(row[altitude_col])
            name_eng = row[name_eng_col]
            formula = handle_float(row[formula_col])
            row_dict = {index: {"longitude": longitude, "latitude": latitude,
                                "altitude": altitude, "name_eng": name_eng,
                                "formula": formula}}
            provider_data.append(row_dict)
        elif row[0] == '' and len(provider_data) != 0:
            providers.append({provider: provider_data})
            provider_data = []
        if i == rows_amount - 1:
            providers.append({provider: provider_data})
    return providers


data = xls_file_extractor(res_filename)
print()
