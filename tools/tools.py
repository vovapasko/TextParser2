import logging
import traceback
from datetime import timedelta, datetime

import configs


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
