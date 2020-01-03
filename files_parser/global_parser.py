import logging
import traceback

from files_parser.parser_tools import extract_data_from_file


def handle_data(excel_data, converted_data):
    # todo think how to handle these data
    try:
        for file_key, file_values in converted_data.items():
            logging.info(f"Start handling data in converted Python data in {file_key} file")
            for value in file_values:
                print(value)
    except Exception:
        logging.exception("Something went wrong here")
        logging.error(traceback.format_exc())


def parse(filename_dir, filenames, data, provider_key):
    logging.info(f"Start getting data for provider {provider_key}")
    converted_data = extract_data_from_file(filename_dir, filenames)
    logging.info(f"The data was parsed from {len(filenames)} files")
    for i in range(len(filenames)):
        logging.info(f"{i + 1}. {filenames[i]}")
    try:
        handle_data(data, converted_data)
    except Exception:
        logging.error("Error happened while handling data")
        logging.error(traceback.format_exc())
        raise Exception
