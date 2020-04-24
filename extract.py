"""This python code read the .csv file and extract information from it. 
"""
import os
import csv
from natsort import natsorted
import numpy as np
import pandas as pd

# Change directory to data folder
os.chdir("data")
# Grab all the files so you can iterate through
files = os.listdir()
# I want to use the earliest day to extract the basic header because it has the most information.
files = natsorted(files, reverse=True)

# iterate through file
for file in files:
    print(f"working on file:{file}")
    with open(file, "r") as read_file:
        # csv_file is a list of list
        csv_file = csv.reader(read_file, delimiter=",")
        # Each row is a list
        category_name = ""
        value = ""
        city_cases = []
        combined_categories = []

        for row in csv_file:
            # removing leading and trailing white space
            row = list(map(str.strip, row))
            row = list(map(str.lower, row))  # create lower case
            # Looking at the file structure, there is a category for green card application,
            # As well as the result of application for each category, hence concatination would be
            # appropriate to increase consistency and uniformity
            if "family-based" in row or "family-based1" in row:  # pre-2017qtr1 has family-based1, hence the option
                application_categories = row  # for green card category
                application_results = next(csv_file)  # for application status
                found = False  # flag

                # For concatinating the category and result
                for category, status in zip(
                    application_categories, application_results
                ):
                    # Checking the condition, if category name is appear, store it as the current category name
                    # If not, then use the previous category name
                    # Then, concatinate the category name and the status
                    # For family based green card
                    if "family" in category:
                        category_name = "Family"
                        # family should come first, hence the flag is true
                        found = True
                    # For employment based green card
                    elif "employment" in category:
                        category_name = "Employment"
                    # For humanitarian based green card
                    elif "humanitarian" in category:
                        category_name = "Humanitarian"
                    # For other category
                    elif "other" in category:
                        category_name = "Other"
                    # For total count of application
                    elif "total" in category:
                        category_name = "Total"
                    # For first couple empty cases
                    elif found == False:
                        pass

                    # There are some numbers after the result (i.e. Application2) so strip those
                    status = "".join(i for i in status if not i.isdigit())
                    value = category_name + ":" + status
                    combined_categories.append(value)

            # If it finds the section of the total number of case
            if "total" in row[0]:
                total_case_numbers = row

            # For looping through states
            # if initial state, alabama, or alaska for pre-2017_qtr3
            if row[0] == "alabama" or row[0] == "alaska":
                while row[1] != "vermont":  # Loop until final city, vermont
                    # if the state column is not empty, meaning this line is state
                    if (row[0] != ""):
                        # grab the state name, make it title
                        state_name = row[0].title()
                    # if the state column is empty, meaning this line is city
                    elif (row[0] == ""):
                        row_with_state = row
                        # adding the state name to the initial part
                        row_with_state[0] = state_name
                        # initialize the city name
                        row_with_state[1] = row_with_state[1].title()
                        # capitalize state abbreviation
                        row_with_state[2] = row_with_state[2].upper()
                        # Add to state list
                        city_cases.append(row_with_state)
                    row = next(csv_file)
                    # removing leading and trailing white space
                    row = list(map(str.strip, row))
                    row = list(map(str.lower, row))  # create lower case

        # Insert header for state, city and abbreviation
        combined_categories[0:3] = ["State", "City", "Abbreviation"]
        city_cases = np.array([np.array(x)[0:23] for x in city_cases])
        combined_categories = combined_categories[0:23]
        print(city_cases)
        print(combined_categories)
        df = pd.DataFrame(data=city_cases)

    # break
