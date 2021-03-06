import os
import traceback

import xlrd
import logging

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
            logging.error("Incorrect value in excel file")
            logging.error(traceback.format_exc())
            raise Exception('There is xlsx not numerical value in excel file')


def get_xlsfile_data(filename):
    wb = xlrd.open_workbook(filename)
    sheet = wb.sheet_by_index(0)
    rows_amount = sheet.nrows
    providers = {}
    provider_data = {}
    provider = ''
    for i in range(2, rows_amount):
        row = sheet.row_values(i)
        if row[0] != '':
            provider = row[provider_col]
            index = row[index_col]
            try:
                longitude = handle_float(row[longitude_col])
                latitude = handle_float(row[latitude_col])
                altitude = handle_float(row[altitude_col])
                formula = handle_float(row[formula_col])
            except ValueError:
                logging.error(f"Problem happened in {i} row of your excel file")
            name_eng = row[name_eng_col]
            provider_data[index] = {"longitude": longitude, "latitude": latitude,
                                    "altitude": altitude, "name_eng": name_eng, "formula": formula}
        elif row[0] == '' and len(provider_data) != 0:
            providers[provider] = provider_data
            provider_data = {}
        if i == rows_amount - 1:
            providers[provider] = provider_data
    return providers
