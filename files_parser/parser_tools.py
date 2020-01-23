import math
import traceback
import xml.etree.ElementTree as xml
import logging

import numpy

from exceptions import NoSuchXmlFilesException


def parse_file(file):
    data = {}
    try:
        tree = xml.parse(file)
        root = tree.getroot()
        for child in root:
            values = []
            for subchild in child:
                values.append(float(subchild.attrib['v']))
            data[child.attrib['id']] = values
        return data
    except Exception:
        logging.debug("In parser_tools.parse_file function")
        logging.error(f"Error happened during file {file} parsing")
        logging.error(traceback.format_exc())


def extract_data_from_file(filename_dir, filenames):
    global_data = {}
    for element in filenames:
        filename = (filename_dir / (element + '.xml'))
        converted_data = parse_file(filename)
        global_data[filename] = converted_data
    if all(value is None for value in global_data.values()):
        raise NoSuchXmlFilesException("There are no xml files with this provider")
    return global_data


def get_list_middle_value(values: list):
    mean_value = numpy.mean(values)
    if math.isnan(mean_value):
        return None
    return mean_value


def get_all_keys_from_dict(param_dict):
    tmp_keys = []
    for file_key, file_value in param_dict.items():
        for key, value in file_value.items():
            tmp_keys.append(key)
    return set(tmp_keys)


def find_mean_of_intervals(param_dict):
    """This method finds mean value for each sublist in every index """
    return_dict = {}
    for key, value in param_dict.items():
        return_dict[key] = get_list_middle_value(value)
    return return_dict


def remove_empty_dicts(full_interval_dict):
    new_dict = dict()
    """Needed for checking the situation where all elements from index didn't pass validation"""
    for key, value in full_interval_dict.items():
        if len(value) > 0:
            new_dict[key] = value
    return new_dict
