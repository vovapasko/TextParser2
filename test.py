import logging

import credentials
from files_parser.global_parser import parse
from tools import excel_tools
from tools.filename_generators import generate_filenames, generate_log_filename


def run(test_key, date, hour, test_filedir):
    current_hour = hour
    current_date = date
    logfilename = generate_log_filename()
    logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', filename=logfilename, level=logging.DEBUG)
    logging.info("Started test mode")
    data = excel_tools.get_xlsfile_data(credentials.res_filename)
    logging.info(f"Data extracted from {credentials.res_filename} successfully")
    filenames = {}
    filenames[test_key] = (generate_filenames(test_key, current_date, current_hour))
    parse(test_filedir, filenames[test_key], data[test_key])


if __name__ == '__main__':
    test_filedir = credentials.home_project_directory / "rubbish"
    run('snpp0', "25.11.2019", "08", test_filedir)
