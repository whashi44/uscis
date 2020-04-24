import os
import re

"""
This is a python script to rename files because the original file name had inconsistency
Also it remove other files that is not useful for analysis 
"""


os.chdir("data")
# Get all the files
all_files = os.listdir()
# Extracting useful files
files = [file for file in all_files if "fy" in file]
remove_files = [file for file in all_files if "fy" not in file]

# # Removing files
# for file in remove_files:
#     os.remove(file)
#     print(f"Deleted file: {file}")

years = []
quarters = []

# Find year and quarter information from file
for file in files:
    numbers = re.findall(
        r"\d+", file  # for number
    )  # 0th is I485, 1st is fiscal year, 2nd is quarter
    years.append(numbers[1])
    quarters.append(numbers[2])

# Rename files to uniform format
for file, year, quarter in zip(files, years, quarters):
    print(f"Changing the filename: {file}")
    new_name = f"I485_data_fy{year}_qtr{quarter}.csv"
    os.rename(file, new_name)
    print(f"Changed to: {new_name}")
