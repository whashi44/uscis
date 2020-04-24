import os
import re
import shutil
"""
This is a python script to rename files because the original file name had inconsistency
Also it remove other files that is not useful for analysis 

"""
data_path = "data"
raw_path = "raw"

try:
    print(f"Making folder: {data_path}")
    os.mkdir(data_path)
except FileExistsError:
    pass
finally:
    os.chdir(raw_path)
    print(f"Changed directory to: {raw_path}")

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
    print(f"Copying and renaming the filename from: \n{file}")
    new_name = f"I485_data_fy{year}_qtr{quarter}.csv"
    shutil.copyfile(file, f"../{data_path}/{new_name}")
    print(f"To: {new_name}")

# remove special file, which has inconsistent format
print(f"Removing special file, the 2013 quarter 3, due to its inconsistent format")
os.remove(f"../{data_path}/I485_data_fy2013_qtr3.csv")
