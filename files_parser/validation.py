from files_parser.validation_constants import *


def correct_interval_value(interval_value, excel_value):
    multiplier = excel_value['formula']
    new_value = interval_value * multiplier
    return new_value <= boundary_interval_value


def correct_whole_interval_value(value):
    return value <= boundary_whole_interval_value
