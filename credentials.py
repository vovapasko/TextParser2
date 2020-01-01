import os
import pathlib

path_to_files = ""
home_project_directory = pathlib.Path(__file__).parent
logs_dir = home_project_directory / "logs"
res_dir = home_project_directory / "res"
res_filename = res_dir / "data.xls"
