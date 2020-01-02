import credentials
from files_parser.global_parser import parse
from tools import excel_tools
from tools.filename_generators import generate_filenames, generate_log_filename
import logging


def start():
    logfilename = generate_log_filename()
    logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', filename=logfilename, level=logging.DEBUG)
    current_hour = "15"
    current_date = "25.11.2019"
    data = excel_tools.get_xlsfile_data(credentials.res_filename)
    logging.info(f"Data extracted from {credentials.res_filename} successfully")
    filenames = {}
    for provider_key, value in data.items():
        filenames[provider_key] = (generate_filenames(provider_key, current_date, current_hour))
    for provider_key, value in data.items():
        parse(credentials.path_to_files, filenames[provider_key], value, provider_key)


if __name__ == '__main__':
    start()
