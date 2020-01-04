"""
This file and this package contains all tools for formatting resulting xml tree according to given data
"""
import logging
import traceback

import credentials
from result_xml.final_xml_tools import format_header, format_identification_subtree, hardcode_identification_subtree


def get_result_xml_tree(data: list, excel_data):
    """This function formats xml root element with 4 subtrees:
    header, identification, measurements and locations  """
    header_subtree = format_header()
    try:
        identification_subtree = format_identification_subtree(credentials.xml_identification_tree_data)
    except Exception:
        logging.error("Error while creating id:Identification xml tree")
        traceback.print_exc()
        id_xml_tree = hardcode_identification_subtree()
        logging.info("Created default id:Identification xml tree")