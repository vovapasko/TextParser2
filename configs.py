import os
import pathlib

# this file uses Python 3.x pathlib library.
# For details refer to https://docs.python.org/3/library/pathlib.html

home_project_directory = pathlib.Path(__file__).parent
test_data_directory = home_project_directory / "test_data"
path_to_files = test_data_directory / "danger_data" / "da"
# path_to_files = pathlib.Path("c:/custom_folder/danger_data")
logs_dir = home_project_directory / "logs"
res_dir = home_project_directory / "res"
res_filename = res_dir / "Dovidnyk_NPP_Irmis.xls"
credentials_filename = res_dir / "credentials.xml"
xml_identification_tree_data = res_dir / "id.xml"
output_directory = home_project_directory / "output"