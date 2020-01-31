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


def remove_nans(par_lst):
    """Some lists can contain data with nan values
    This function should delete such values and leave only float data in list
    """
    handled_list = []
    for element in par_lst:
        if not math.isnan(element):
            handled_list.append(element)
    return handled_list


def init_dict(keys) -> dict:
    """Init dict with structure {key: []}"""
    return_dict = {}
    for key in keys:
        return_dict[key] = []
    return return_dict


def log_good_indexes(good_indexes):
    logging.info("--------GOOD INDEXES INFORMATION--------")
    if len(good_indexes) == 0:
        logging.warning("THERE ARE NO GOOD INDEXES. CHECK YOUR DATA")
    else:
        logging.info(f"THERE ARE {len(good_indexes)} INDEXES, WHICH INCLUDED IN FINAL XML")


def log_bad_indexes(good_indexes, all_indexes):
    good_indexes_keys = set(good_indexes.keys())
    all_indexes_keys = set(all_indexes.keys())
    bad_indexes_keys = all_indexes_keys.difference(good_indexes_keys)
    logging.info("--------BAD INDEXES INFORMATION--------")
    if len(bad_indexes_keys) == 0:
        logging.info("THERE ARE NO BAD INDEXES")
    else:
        i = 1
        logging.warning(f"FOUND {len(bad_indexes_keys)} BAD INDEX(ES)")
        for element in bad_indexes_keys:
            logging.warning(f"{i}. {element}")
            i += 1


def log_successfully_parsed_data(python_xml_data):
    i = 0
    logging.info("--------PROVIDERS INFORMATION--------")
    for key, value in python_xml_data.items():
        if value is not None:
            logging.info(f"{i + 1}. {key.stem}")
            i += 1
        else:
            logging.error(f"The data in {key.stem} were damaged or empty")
    logging.info(f"The data was parsed from {i} files")
