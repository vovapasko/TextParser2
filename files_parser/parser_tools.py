import traceback
import xml.etree.ElementTree as et
import logging


def parse_file(file):
    data = {}
    try:
        tree = et.parse(file)
        root = tree.getroot()
        for child in root:
            values = []
            for subchild in child:
                values.append(subchild.attrib['v'])
            data[child.attrib['id']] = values
        return data
    except Exception:
        logging.error(f"Error happened during file {file} parsing")
        logging.error(traceback.format_exc())


def extract_data_from_file(filename_dir, filenames):
    global_data = {}
    for element in filenames:
        filename = (filename_dir / (element + '.xml'))
        converted_data = parse_file(filename)
        global_data[filename] = converted_data
    return global_data
