import os
from datetime import datetime
from pathlib import Path

from credentials import logs_dir, home_project_directory
from tools.tools import generate_time_intervals


def generate_filenames(index, date, hour):
    """
    Generates list of filenames according to the template
    index_start-time=date-"hour-1_00_00"_end_time=date-"hour-1_05_00"
    ...
    index_start-time=date-"hour-1_55_00"_end_time=date-"hour_00_00"
    """
    time_intervals = generate_time_intervals(hour)
    filenames = []
    for i in range(len(time_intervals) - 1):
        string = f"{index}_start-time={date}-{time_intervals[i]}_end-time={date}-{time_intervals[i + 1]}"
        filenames.append(string)
    return filenames


def generate_log_filename():
    filename = datetime.now().strftime("%Y-%m-%d %X") + '.log'
    new_str = filename.replace(' ', '_').replace(':', '_')
    strdaw = logs_dir / new_str
    return strdaw
