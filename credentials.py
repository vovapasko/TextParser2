import os
import pathlib

# this file uses Python 3.x pathlib library.
# For details refer to https://docs.python.org/3/library/pathlib.html

path_to_files = pathlib.Path("C / Users / charl / OneDrive / Документы / Arbeit / Завдання / npp")
home_project_directory = pathlib.Path(__file__).parent
logs_dir = home_project_directory / "logs"
res_dir = home_project_directory / "res"
res_filename = res_dir / "data.xls"
