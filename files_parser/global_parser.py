import logging

from files_parser.single_file_parser import parse_file


def parse(filename_dir, filenames, data):
    global_data = {}
    for element in filenames:
        filename = str(filename_dir / (element + '.xml'))
        converted_data = parse_file(filename)
        global_data[filename] = converted_data
    print()