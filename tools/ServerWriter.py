"""This file contains class which responds for writing data to ftp server
"""
import logging

import pysftp as pysftp
import xml.etree.ElementTree as xml

from configs import credentials_filename


class Writer:
    def __init__(self):
        self.ftp_host = self.get_data_from_cred('host')
        self.ftp_username = self.get_data_from_cred('username')
        self.ftp_password = self.get_data_from_cred('password')
        self.remote_folder = self.get_data_from_cred('folder')

    def write_to_sftp(self, filename):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection(host=self.ftp_host, username=self.ftp_username, password=self.ftp_password) as sftp:
            with sftp.cd(self.remote_folder):  # temporarily chdir to public
                sftp.put(filename)  # upload file to public/ on remote

    def get_data_from_cred(self, key):
        try:
            file = xml.parse(credentials_filename)
            root = file.getroot()
            value = root.find(key).text
            return value
        except Exception:
            logging.error(f"Error happened while getting {key} from the credentials file")
            return key
