# Program to extract number
# of rows using Python
import os

import xlrd
from credentials import home_project_directory, res_dir, res_filename

# Give the location of the file
loc = (os.path.join(home_project_directory, res_dir, res_filename))

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

sheet.cell_value(0, 0)

print(sheet.row_values(2))
