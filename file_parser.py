import logging


def parse(filename_dir, filenames, data):
    for filename in filenames:
        file = open(filename_dir / (filename + '.xml'), 'r')
        dat = file.read()

