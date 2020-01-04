import logging
import traceback

import credentials
from files_parser.global_parser import parse
from tools import excel_tools
from tools.filename_generators import generate_filenames, generate_log_filename
from result_xml.result_xml_formatting import get_result_xml_tree


def run(test_key, date, hour, test_filedir):
    current_hour = hour
    current_date = date
    logfilename = generate_log_filename()
    logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', filename=logfilename, level=logging.DEBUG)
    logging.info("Started test mode")
    excel_data = excel_tools.get_xlsfile_data(credentials.res_filename)
    logging.info(f"Data extracted from {credentials.res_filename} successfully")
    filenames = dict()
    filenames[test_key] = generate_filenames(test_key, current_date, current_hour)
    handled_data = list()
    handled_data.append(parse(test_filedir, filenames[test_key], excel_data[test_key], test_key))
    final_xml = get_result_xml_tree(handled_data, excel_data, date, hour)
    logging.info("Successfully created result xml file")
    try:
        final_xml.write(credentials.output_directory / 'test.xml', encoding="utf-8", xml_declaration=True, method="xml")
        logging.info(f"Successfully created the - {credentials.output_directory / 'test.xml'} xml file")
    except Exception:
        logging.error("Error while creating result xml file")
        logging.error(traceback.format_exc())
        traceback.print_exc()



if __name__ == '__main__':
    test_filedir = credentials.home_project_directory / "rubbish"
    run('snpp0', "25.11.2019", "08", test_filedir)
