import traceback
import xml.etree.ElementTree as et
import logging

import numpy


def parse_file(file):
    data = {}
    try:
        tree = et.parse(file)
        root = tree.getroot()
        for child in root:
            values = []
            for subchild in child:
                values.append(float(subchild.attrib['v']))
            data[child.attrib['id']] = values
        return data
    except Exception:
        logging.error(f"Error happened during file {file} parsing")
        logging.error(traceback.format_exc())


def extract_data_from_file(filename_dir, filenames):
    global_data = {}
    for element in filenames:
        filename = (filename_dir / (element + '.xml'))
        converted_data = parse_file(filename)
        global_data[filename] = converted_data
    return global_data


def log_uncommon_elements(excel_data, converted_data):
    excel_keys_set = set(excel_data.keys())
    for file_key, file_values in converted_data.items():
        file_values_keys_set = set(file_values.keys())
        set_difference = file_values_keys_set.difference(excel_keys_set)
        logging.warning(
            f"There are {len(set_difference)} amount of indexes which are not in excel file ({file_key.stem})."
            f" These files won't be included in final .xml file")
        for element, i in zip(set_difference, range(len(set_difference))):
            logging.info(f"{i + 1}. {element}")


def get_middle_value(values):
    return float("%.2f" % numpy.mean(values))  # finds mean and rounds to 2 signs after dot


def get_all_keys_from_dict(param_dict):
    tmp_keys = []
    for file_key, file_value in param_dict.items():
        for key, value in file_value.items():
            tmp_keys.append(key)
    return set(tmp_keys)
