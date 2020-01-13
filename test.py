import logging
import traceback
from datetime import datetime

import credentials
from files_parser.global_parser import parse
from tools import excel_tools
from tools.filename_generators import generate_filenames, generate_log_filename, generate_output_xml_filename
from result_xml.result_xml_formatting import get_result_xml_tree
from tools.tools import write_xml_to_file

program_start_time = datetime.now()
custom_hour = 9
custom_year = 2019
custom_month = 11
custom_day = 25
custom_datetime = datetime(custom_year, custom_month, custom_day, custom_hour, 0, 0)


def start(test_key, custom_datetime, test_filedir):
    logfilename = generate_log_filename(program_start_time)
    logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', filename=logfilename, level=logging.DEBUG)
    logging.debug("Started test mode")
    excel_data = excel_tools.get_xlsfile_data(credentials.res_filename)
    logging.info(f"Data extracted from {credentials.res_filename} successfully")
    filenames = dict()
    filenames[test_key] = generate_filenames(test_key, custom_datetime)
    handled_data = list()
    handled_data.append(parse(test_filedir, filenames[test_key], excel_data[test_key], test_key))
    final_xml = get_result_xml_tree(handled_data, excel_data, custom_datetime)
    logging.info("Successfully created result xml file")
    write_xml_to_file(final_xml, credentials.output_directory / generate_output_xml_filename(program_start_time))


if __name__ == '__main__':
    test_filedir = credentials.home_project_directory / "rubbish"
    start('snpp0', custom_datetime, test_filedir)
