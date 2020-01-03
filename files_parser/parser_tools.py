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


def get_middle_value(values):
    return numpy.mean(values)  # finds mean and rounds to 2 signs after dot


def get_all_keys_from_dict(param_dict):
    tmp_keys = []
    for file_key, file_value in param_dict.items():
        for key, value in file_value.items():
            tmp_keys.append(key)
    return set(tmp_keys)
