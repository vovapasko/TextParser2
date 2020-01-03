import logging
import traceback

from files_parser.parser_tools import extract_data_from_file, log_uncommon_elements, get_middle_value, \
    get_all_keys_from_dict


def get_converted_xml_data(python_xml_data: dict) -> dict:
    new_converted_data = {}
    for file_key, file_values in python_xml_data.items():
        for key, values in file_values.items():
            middle_value = get_middle_value(values)
            new_converted_data[key] = middle_value
    return new_converted_data


def handle_converted_xml_data(data_to_handle: dict, excel_data: dict) -> dict:
    """This function contains all logic for handling parsed from xml file data."""
    excel_data_keys_set = set(excel_data.keys())
    data_to_handle_keys_set = get_all_keys_from_dict(data_to_handle)
    log_uncommon_elements(excel_data, data_to_handle)
    work_set = excel_data_keys_set.intersection(
        data_to_handle_keys_set)  # indexes which are in excel and xml file simultaneously

    pass


def get_handled_data(excel_data, python_xml_data):
    full_converted_xml_data = {}  # has the same structure as python_xml_data but with counted for 5 minutes meant numbers
    handled_xml_data = {}
    try:
        for file_key, file_values in python_xml_data.items():
            logging.info(f"Start handling data in converted Python data in {file_key.stem} file")
            one_file_converted_xml_data = get_converted_xml_data(python_xml_data)
            full_converted_xml_data[file_key] = one_file_converted_xml_data
        handled_xml_data = handle_converted_xml_data(full_converted_xml_data, excel_data)
    except Exception:
        logging.exception("Something went wrong here")
        logging.error(traceback.format_exc())
        print(traceback.format_exc())


def parse(filename_dir, filenames, data, provider_key):
    logging.info(f"Start getting data for provider {provider_key}")
    python_xml_data = extract_data_from_file(filename_dir, filenames)
    logging.info(f"The data was parsed from {len(filenames)} files")
    for i in range(len(filenames)):
        logging.info(f"{i + 1}. {filenames[i]}")
    try:
        get_handled_data(data, python_xml_data)
    except Exception:
        logging.error("Error happened while handling data")
        logging.error(traceback.format_exc())
        raise Exception
