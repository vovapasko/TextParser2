from datetime import datetime

import configs
from files_parser.global_parser import parse
from tools import excel_tools
from tools.filename_generators import generate_filenames, generate_log_filename, generate_output_xml_filename
import logging
from result_xml.result_xml_formatting import get_result_xml_tree
from tools.tools import write_xml_to_file, handle_datetime

program_start_time = current_datetime = datetime.now()
custom_hour = 9
custom_year = 2019
custom_month = 11
custom_day = 25
custom_datetime = datetime(custom_year, custom_month, custom_day, custom_hour, 0, 0)
filenames = {}
handled_data = []
handled_data_providers = []
bad_providers = []


def start(par_datetime=current_datetime):
    par_datetime = handle_datetime(par_datetime)
    logfilename = generate_log_filename(program_start_time)
    logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', filename=logfilename, level=logging.DEBUG)
    excel_data = excel_tools.get_xlsfile_data(configs.res_filename)
    logging.debug(f"Data extracted from {configs.res_filename} successfully")
    for provider_key, value in excel_data.items():
        filenames[provider_key] = (generate_filenames(provider_key, par_datetime))
    for provider_key, value in excel_data.items():
        tmp = parse(configs.path_to_files, filenames[provider_key], value, provider_key)
        if tmp is not None:
            handled_data.append(tmp)
            handled_data_providers.append(provider_key)
        else:
            bad_providers.append(provider_key)
    logging.info(f"Started forming data with {len(handled_data_providers)} providers: ")
    for i, provider in zip(range(len(handled_data_providers)), handled_data_providers):
        logging.info(f"{i + 1}. {provider}")
    if len(bad_providers) > 0:
        logging.warning(f"There is {len(bad_providers)} provider(s) which data program can't parse: ")
        for i, provider in zip(range(len(bad_providers)), bad_providers):
            logging.warning(f"{i + 1}. {provider}")
    result_xlm = get_result_xml_tree(handled_data, excel_data, par_datetime)
    write_xml_to_file(result_xlm, configs.output_directory / generate_output_xml_filename(program_start_time))


if __name__ == '__main__':
    start(par_datetime=custom_datetime)  # remove a parameter if you want a custom datetime
