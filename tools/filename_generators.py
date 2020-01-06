import os
from datetime import datetime
from pathlib import Path

from credentials import logs_dir, home_project_directory
from tools.tools import split_datetime_to_deltas


def get_correct_string(par_datetime):
    return par_datetime.strftime("%Y-%m-%d %X")


def generate_filenames(index, given_datetime: datetime):
    """
    Generates list of filenames according to the template
    index_start-time=date-"hour-1_00_00"_end_time=date-"hour-1_05_00"
    ...
    index_start-time=date-"hour-1_55_00"_end_time=date-"hour_00_00"
    """
    time_intervals = split_datetime_to_deltas(given_datetime)
    filenames = []
    for i in range(len(time_intervals) - 1):
        string = f"{index}_start-time={datetime.strftime(time_intervals[i], '%d.%m.%Y-%H_%M_%S')}_end-time={datetime.strftime(time_intervals[i + 1], '%d.%m.%Y-%H_%M_%S')}"
        filenames.append(string)
    return filenames


def generate_log_filename():
    filename = datetime.now().strftime("%Y-%m-%d %X") + '.log'
    new_str = filename.replace(' ', '_').replace(':', '_')
    strdaw = logs_dir / new_str
    return strdaw


def generate_output_xml_filename(current_datetime):
    new_str = str(current_datetime).replace(' ', '_').replace(':', '_')
    return new_str + ".xml"
