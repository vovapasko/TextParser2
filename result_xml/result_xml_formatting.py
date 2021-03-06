"""
This file and this package contains all tools for formatting resulting xml tree according to given data
"""
import logging
import traceback

import configs
from result_xml.final_xml_tools import format_header, format_identification_subtree, hardcode_identification_subtree, \
    combine_xml, format_measurements_subtree, format_locations_subtree


def get_result_xml_tree(measurement_data: list, excel_data, end_measuring_timestamp):
    """This function formats xml root element with 4 subtrees:
    header, identification, measurements and locations  """
    logging.debug("In get_result_xml_tree. Format header subtree")
    header_subtree = format_header()
    try:
        logging.debug("Format identification subtree from file")
        identification_subtree = format_identification_subtree(configs.xml_identification_tree_data)
    except Exception:
        logging.error("Error while creating id:Identification xml tree")
        traceback.print_exc()
        logging.debug("Format hardcoded identification subtree")
        identification_subtree = hardcode_identification_subtree()
        logging.info("Created default id:Identification xml tree")
    measurements_subtree = format_measurements_subtree(measurement_data, end_measuring_timestamp)
    locations_subtree = format_locations_subtree(measurement_data, excel_data)
    result_tree = combine_xml(header_subtree, [identification_subtree, measurements_subtree, locations_subtree])
    return result_tree
