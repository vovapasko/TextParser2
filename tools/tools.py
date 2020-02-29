import logging
import os
import traceback
from datetime import timedelta, datetime
import pytz
import xml.etree.ElementTree as xml

from configs import credentials_filename


def write_xml_to_file(final_xml, write_to_path):
    try:
        final_xml.write(write_to_path, encoding="utf-8", xml_declaration=True, method="xml")
        logging.info(f"Successfully created the - {write_to_path} xml file")
    except Exception:
        logging.error("Error while creating result xml file")
        logging.error(traceback.format_exc())
        traceback.print_exc()


def split_datetime_to_deltas(end_datetime):
    minutedelta = timedelta(minutes=5)
    date_x = end_datetime - timedelta(hours=1)
    five_min_timestamps = [date_x]
    while date_x < end_datetime:
        date_x += minutedelta
        five_min_timestamps.append(date_x)
    return five_min_timestamps


def handle_datetime(par_datetime: datetime) -> datetime:
    new_datetime = datetime(par_datetime.year, par_datetime.month, par_datetime.day, par_datetime.hour, 0, 0)
    """Function handles datetime if given datetime was not custom. It equals minutes and seconds to 0."""
    return convert_to_utc(new_datetime)


def convert_to_utc(par_datetime):
    new_time = par_datetime.astimezone(pytz.UTC)
    return new_time


def get_data_from_cred(key, subroot):
    """subroot is one of the main subfolders where function should search a key. For example <ServerData>"""
    try:
        file = xml.parse(credentials_filename)
        root = file.getroot()
        subdir = root.find(subroot)
        value = subdir.find(key).text
        return value
    except Exception:
        logging.error(f"Error happened while getting {subroot}-{key} from the credentials file")
        return key


def handle_mail_content(one_interval_bad_values, whole_interval_bad_values):
    logging.debug("In handle_mail_content function")
    logging.debug(whole_interval_bad_values)
    msg = ""
    for elements in one_interval_bad_values:
        for elem in elements:
            msg += elem["message"]
            msg += os.linesep
    for elements in whole_interval_bad_values:
        for elem in elements:
            msg += elem["message"]
            msg += os.linesep
    return msg
