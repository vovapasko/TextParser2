import logging

from files_parser.parser_tools import extract_data_from_file


def handle_data(excel_data, converted_data):


    pass


def parse(filename_dir, filenames, data):
    converted_data = extract_data_from_file(filename_dir, filenames)
    logging.info(f"The data was parsed from {len(filenames)} files")
    for i in range(len(filenames)):
        logging.info(f"{i + 1}. {filenames[i]}")
    handle_data(data, converted_data)