import logging
import math
import traceback

from exceptions import NoSuchXmlFilesException, NoSuchOneXmlFileException
from files_parser.validation_constants import boundary_interval_value, boundary_whole_interval_value
from files_parser.parser_tools import extract_data_from_file, get_list_middle_value, \
    get_all_keys_from_dict, find_mean_of_intervals, remove_empty_dicts, remove_nans, init_dict, log_good_indexes, \
    log_bad_indexes, log_successfully_parsed_data
from files_parser.validation import correct_interval_value, correct_whole_interval_value


def get_converted_xml_data(file_values: dict) -> dict:
    new_converted_data = {}
    if file_values is None:
        raise NoSuchOneXmlFileException()
    for key, values in file_values.items():
        handled_list = remove_nans(values)
        middle_value = get_list_middle_value(handled_list)
        if middle_value is not None:
            new_converted_data[key] = middle_value
    return new_converted_data


def handle_converted_xml_data(data_to_handle: dict, excel_data: dict) -> dict:
    """This function contains all logic for handling parsed from xml file data."""
    logging.debug("In handle_converted_xml_data function")
    excel_data_keys_set = set(excel_data.keys())
    data_to_handle_keys_set = get_all_keys_from_dict(data_to_handle)
    work_set = excel_data_keys_set.intersection(
        data_to_handle_keys_set)  # indexes which are in excel and xml file simultaneously
    full_interval_dict = init_dict(work_set)
    # handling data for time interval
    for file_key, file_value in data_to_handle.items():
        logging.debug(f"Start data converting in {file_key.stem}")
        for index in work_set:
            interval_value = file_value.get(index)
            excel_value = excel_data.get(index)
            if interval_value is not None and excel_value is not None:
                if correct_interval_value(interval_value, excel_value):
                    multiplier = excel_value['formula']
                    converted_value = interval_value * multiplier
                    full_interval_dict["good_values"][index].append(converted_value)
                else:
                    warn_message = f"Interval value {interval_value} is more than boundary value " \
                                   f"{boundary_interval_value} on 5 minutes interval"
                    full_interval_dict["high_one_interval_values"].append(
                        {"value": interval_value, "index": index, "file": file_key.stem, "message": warn_message})
                    logging.warning(warn_message)
                    logging.warning(f"This value is in index - {index} and in file - {file_key.stem}")
                    logging.warning("This value won't be included in result xml file")
            else:
                logging.error(f"Error with data in {file_key.stem} with provider - {index}")
                logging.error(f"This happened probably because the entry file is empty or has none values")
    # handling data for the whole time
    handled_full_interval_dict = remove_empty_dicts(full_interval_dict["good_values"])
    full_interval_dict["good_values"] = find_mean_of_intervals(handled_full_interval_dict)

    for key, value in list(full_interval_dict["good_values"].items()):
        if not correct_whole_interval_value(value):
            full_interval_dict["good_values"].pop(key, None)
            warn_message = f"Final value {value} is is more than boundary value {boundary_whole_interval_value} on 1 hour interval"
            full_interval_dict["high_whole_interval_values"].append({"value": boundary_whole_interval_value, "index": key, "message": warn_message})
            logging.warning(warn_message)
            logging.warning(f"This value is in index - {key}")
            logging.warning("This value won't be included in result xml file")
    logging.debug("In the end of handle_converted_xml_data function")
    return full_interval_dict


def get_handled_data(excel_data, python_xml_data):
    full_converted_xml_data = {}  # has the same structure as python_xml_data but with counted for 5 minutes meant numbers
    logging.debug("In get_handled_data function")
    try:
        for file_key, file_values in python_xml_data.items():
            logging.debug(f"Start handling data in converted Python data in {file_key.stem} file")
            try:
                one_file_converted_xml_data = get_converted_xml_data(file_values)
                full_converted_xml_data[file_key] = one_file_converted_xml_data
                logging.debug(f"Successfully handled data in converted Python data in {file_key.stem} file")
            except NoSuchOneXmlFileException:
                logging.error(f"There is no {file_key.stem} file")
        handled_xml_data = handle_converted_xml_data(full_converted_xml_data, excel_data)
        logging.debug(
            "In the end of get_handled_data function. If you see this, data was handled without critical errors")
        logging.info("Data from python xml data is handled successfully")
        return handled_xml_data
    except Exception:
        logging.exception("Something went wrong here")
        logging.error(traceback.format_exc())
        print(traceback.format_exc())


def parse(filename_dir, filenames, data, provider_key):
    logging.info(f"Start getting data for provider {provider_key}")
    try:
        python_xml_data = extract_data_from_file(filename_dir, filenames)
        try:
            handled_data = get_handled_data(data, python_xml_data)
            logging.info(f"Data from provider '{provider_key}' handled successfully")
            log_successfully_parsed_data(python_xml_data)
            log_good_indexes(handled_data["good_values"])
            log_bad_indexes(handled_data["good_values"], data)
            return handled_data
        except Exception:
            logging.error("Error happened while handling data")
            logging.error(traceback.format_exc())
            raise Exception
    except NoSuchXmlFilesException:
        logging.critical("There are no files with the next names.")
        for i in range(len(filenames)):
            logging.error(f"{i + 1}. {filenames[i]}")
        logging.error("This may happen because there are no such a files by your provider name.")
        logging.error(f"Check whether you have data from provider '{provider_key}'")
