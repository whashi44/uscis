"""This python code read the .csv file and extract information from it, then save the file
"""
import os
import csv
from natsort import natsorted
import numpy as np
import pandas as pd
import re
# Change directory to data folder
try:
    os.chdir("data")
except FileNotFoundError:
    raise FileNotFoundError

# Grab all the files so you can iterate through
files = os.listdir()
# I want to use the newest report to extract the basic header because it has the most information.
files = natsorted(files, reverse=True)

# Grab header information
with open(files[0], "r") as read_file:
    # read file as csv
    csv_file = csv.reader(read_file, delimiter=",")
    header = []

    for row in csv_file:
        # removing leading and trailing white space
        row = list(map(str.strip, row))
        # lower casing all the item to avoid word mismatch
        row = list(map(str.lower, row))
        # for special case, 2019 qtr 1 and qtr 2
        other_count = 1
        # Looking at the file structure, there is a category for green card application,
        # As well as the result of application for each category, hence concatnate would be
        # appropriate to increase consistency and uniformity
        # pre-2017qtr1 has family-based1, instead of family-based
        if "family-based" in row or "family-based1" in row:
            category_name = ""  # for "family-based", "employment"
            categories = row  # for green card category
            results = next(csv_file)  # for application status
            found_family = False  # flag
            found_other = False
            # For concatinating the category and result
            for category, status in zip(
                categories, results
            ):
                # Checking the condition, if category name appears, store the category name
                # If not, then use the previous category name
                # Then, cancatnate the category name and the status with ":"

                # For family based green card
                if "family" in category:
                    category_name = "Family"
                    # family should come first, hence the flag is true
                    found_family = True
                # For employment based green card
                elif "employment" in category:
                    category_name = "Employment"
                # For humanitarian based green card
                elif "humanitarian" in category:
                    category_name = "Humanitarian"
                # For other category
                elif "other" in category:
                    category_name = "Other"
                    found_other = True
                # For total count of application
                elif "total" in category:
                    category_name = "Total"
                # For 2019 qtr 1 and qtr 2 with shifted "total"
                elif other_count == 4:
                    category_name = "Total"
                # For keeping track of "other" to make sure "total" is included
                elif found_other:
                    other_count += 1
                # For first couple empty cases
                elif not found_family:
                    pass

                # There are some numbers after the result (i.e. Application2) so strip those
                status = "".join(i for i in status if not i.isdigit())

                # concatnate to create better category
                value = category_name + ":" + status
                header.append(value)

    # Fill those empty header
    header[0:3] = ["State", "City", "Abbreviation"]

    # eliminate those empty strings in the end
    header = header[0:23]

    # Add year and quarter
    header.append("Year")
    header.append("Quarter")


# Grab states and city information
city_cases = []

for file in files:
    print(f"working on file:{file}")
    # Find the year and quarter from the file name
    numbers = re.findall(r"\d+", file  # for number
                         )  # 0th is I485, 1st is fiscal year, 2nd is quarter
    year = numbers[1]
    quarter = numbers[2]

    with open(file, "r") as read_file:
        # csv_file is a list of list
        csv_file = csv.reader(read_file, delimiter=",")

        # Each row is a list
        for row in csv_file:
            # removing leading and trailing white space
            row = list(map(str.strip, row))
            # lower casing for case-insensitive comparison
            row = list(map(str.lower, row))

            # If it finds the section of the total number of case, store that
            if "total" in row[0]:
                total_case_numbers = row

            # For looping through states
            # if the first column(state) is alabama, or alaska for before 2017_qtr3
            if row[0] == "alabama" or row[0] == "alaska":
                # Loop until final city, vermont
                while row[1] != "vermont":
                    # if 1st column is not empty, meaning this row is state
                    if (row[0] != ""):
                        # grab the state name
                        state_name = row[0].title()

                    # if the 1st column is empty, meaning this row is city
                    # some year has repeating the header at the middle of the line, hence 2nd if statement is counter for that (see 2018 qtr 1 Kentucky)
                    elif (row[0] == "" and row[1] != ""):
                        row_with_state = row
                        # adding the state name to the initial part
                        row_with_state[0] = state_name
                        # initialize the city name
                        row_with_state[1] = row_with_state[1].title()
                        # capitalize state abbreviation
                        row_with_state[2] = row_with_state[2].upper()
                        # Some year has empty strings in the end of the row, hence simply substitute
                        try:
                            row_with_state[23] = year
                            row_with_state[24] = quarter
                        # Some states do not have empty strings in the of the row, hence handle that
                        except IndexError:
                            # for pre 2014, there is no city abbreviation, insert empty string to avoid index error later on
                            if year == "2014":
                                row_with_state.insert(2, "")

                            # other case append instead of inject
                            row_with_state.append(year)
                            row_with_state.append(quarter)

                        # Add to state list
                        city_cases.append(row_with_state)

                    # keep checking the next row
                    row = next(csv_file)
                    # removing leading and trailing white space
                    row = list(map(str.strip, row))
                    row = list(map(str.lower, row))  # create lower case

# convert the list of list to array of array
city_cases = np.array([np.array(x)[0:25] for x in city_cases])
# convert the list to array
header = np.array(header)
# Dataframe for easier manipulation
df = pd.DataFrame(data=city_cases, columns=header)
# save to csv file
# df.to_csv('I485_data_2014-2019.csv')
print(df)
