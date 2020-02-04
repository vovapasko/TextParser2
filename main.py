import traceback
from datetime import datetime, timedelta

import configs
from files_parser.global_parser import parse
from tools import excel_tools
from tools.MailSender import MailSender
from tools.ServerWriter import ServerWriter
from tools.filename_generators import generate_filenames, generate_log_filename, generate_output_xml_filename
import logging
from result_xml.result_xml_formatting import get_result_xml_tree
from tools.tools import write_xml_to_file, handle_datetime, convert_to_utc, handle_mail_content

program_start_time = current_datetime = datetime.now()
# please note that hour you typed below will be converted to utc
custom_hour = 20  # will generate filenames for [custom_hour - 1; custom_hour]
custom_year = 2019
custom_month = 7
custom_day = 2
custom_datetime = datetime(custom_year, custom_month, custom_day, custom_hour, 0, 0)
filenames = {}
handled_data = []
handled_data_providers = []
bad_providers = []
one_interval_bad_values = []
whole_interval_bad_values = []


def start(par_datetime=current_datetime, write_to_server=False, send_mail=False):
    par_datetime = handle_datetime(par_datetime)
    logfilename = generate_log_filename(program_start_time)
    logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', filename=logfilename, level=logging.DEBUG)
    try:
        excel_data = excel_tools.get_xlsfile_data(configs.res_filename)
        logging.debug(f"Data extracted from {configs.res_filename} successfully")
    except Exception:
        logging.critical("Error happened while was trying to extract data from Excel file. Please check it.")
        logging.error(traceback.format_exc())
        return None
    logging.info(f"Start extracting xml files from directory {configs.path_to_files}")
    for provider_key, value in excel_data.items():
        filenames[provider_key] = (generate_filenames(provider_key, par_datetime))
    for provider_key, value in excel_data.items():
        tmp = parse(configs.path_to_files, filenames[provider_key], value, provider_key)
        if tmp is not None:
            handled_data.append(tmp["good_values"])
            handled_data_providers.append(provider_key)
            if len(tmp["high_one_interval_values"]) > 0:
                one_interval_bad_values.append(tmp["high_one_interval_values"])
            if len(tmp["high_whole_interval_values"]) > 0:
                whole_interval_bad_values.append(tmp["high_whole_interval_values"])
        else:
            bad_providers.append(provider_key)
    if len(bad_providers) > 0:
        logging.warning(f"There is {len(bad_providers)} provider(s) which data program can't parse: ")
        for i, provider in zip(range(len(bad_providers)), bad_providers):
            logging.warning(f"{i + 1}. {provider}")
    # means that data from all providers are absent and final xml file shouldn't be formatted
    if len(handled_data_providers) == 0:
        logging.error(
            f"THERE ARE NO DATA WITH GIVEN PROVIDERS FOR THE TIME {par_datetime - timedelta(hours=1)} -"
            f" {par_datetime}")
    else:
        logging.info(f"Started forming data with {len(handled_data_providers)} providers: ")
        for i, provider in zip(range(len(handled_data_providers)), handled_data_providers):
            logging.info(f"{i + 1}. {provider}")
        result_xlm = get_result_xml_tree(handled_data, excel_data, par_datetime)
        filename = str(configs.output_directory / generate_output_xml_filename(program_start_time))
        write_xml_to_file(result_xlm, filename)
        if write_to_server:
            writer = ServerWriter()
            writer.write_to_sftp(filename)
        if send_mail and (len(one_interval_bad_values) > 0 or len(whole_interval_bad_values) > 0):
            mailSender = MailSender()
            mailSender.set_subject(configs.mail_subject)
            content = handle_mail_content(one_interval_bad_values, whole_interval_bad_values)
            mailSender.set_content(content)
            mailSender.set_attachment([configs.logs_dir / logfilename])
            mailSender.send_message()


if __name__ == '__main__':
    start(par_datetime=program_start_time, write_to_server=False,
          send_mail=False)  # remove a parameter if you want a custom datetime
