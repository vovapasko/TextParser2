"""This file contains class which responds for writing data to ftp server
"""
import logging
import traceback

import pysftp
import xml.etree.ElementTree as xml

from configs import credentials_filename
from tools.tools import get_data_from_cred


class ServerWriter():
    def __init__(self):
        self.ftp_host = self.get_data_from_cred('host')
        self.ftp_username = self.get_data_from_cred('username')
        self.ftp_password = self.get_data_from_cred('password')
        self.remote_folder = self.get_data_from_cred('remote_folder')
        self.port = int(self.get_data_from_cred('port'))

    def write_to_sftp(self, filename):
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            with pysftp.Connection(host=self.ftp_host, username=self.ftp_username, password=self.ftp_password,
                                   cnopts=cnopts) as sftp:
                with sftp.cd(self.remote_folder):  # temporarily chdir to public
                    sftp.put(filename)  # upload file to public/ on remote
            logging.info("Successfully send the file to sftp server")
        except Exception:
            logging.error(traceback.format_exc())
            logging.error("Error happened while writing file to sftp")
            traceback.print_exc()

    def get_data_from_cred(self, key, subroot="ServerData"):
        return get_data_from_cred(key, subroot)
