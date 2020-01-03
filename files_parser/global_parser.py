import logging
import traceback

from files_parser.parser_tools import extract_data_from_file, log_uncommon_elements, get_middle_value


def get_converted_xml_data(excel_data, python_xml_data):
    new_converted_data = {}
    for file_key, file_values in python_xml_data.items():
        for key, values in file_values.items():
            middle_value = get_middle_value(values)
            new_converted_data[key] = middle_value
    log_uncommon_elements(excel_data, python_xml_data)
    return new_converted_data


def handle_data(excel_data, python_xml_data):
    full_converted_xml_data = {}
    try:
        for file_key, file_values in python_xml_data.items():
            logging.info(f"Start handling data in converted Python data in {file_key.stem} file")
            one_file_converted_xml_data = get_converted_xml_data(excel_data, python_xml_data)
            full_converted_xml_data[file_key] = one_file_converted_xml_data
    except Exception:
        logging.exception("Something went wrong here")
        logging.error(traceback.format_exc())


def parse(filename_dir, filenames, data, provider_key):
    logging.info(f"Start getting data for provider {provider_key}")
    python_xml_data = extract_data_from_file(filename_dir, filenames)
    logging.info(f"The data was parsed from {len(filenames)} files")
    for i in range(len(filenames)):
        logging.info(f"{i + 1}. {filenames[i]}")
    try:
        handle_data(data, python_xml_data)
    except Exception:
        logging.error("Error happened while handling data")
        logging.error(traceback.format_exc())
        raise Exception
