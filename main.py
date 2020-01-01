import credentials
from tools.filename_generators import generate_filenames, generate_log_filename
import logging


def start():
    logfilename = generate_log_filename()
    logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', filename=logfilename, level=logging.DEBUG)
    current_hour = "15"
    current_date = "25.11.2019"
    lst = generate_filenames('rnpp0', current_date, current_hour)
    logging.info(f"Logs are here!")
    print(lst)
    pass


if __name__ == '__main__':
    start()
