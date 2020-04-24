import requests
import csv
import numpy as np
import pandas as pd

# This python code was an attempt to extract information from the uscis I485 data, however realized that there was an easy way to
# download .csv file, hence check out download->rename->extract->

us_state = [
    "Alabama",
    "Alaska",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming",
]

csv_url = "https://www.uscis.gov/sites/default/files/USCIS/Resources/Reports%20and%20Studies/Immigration%20Forms%20Data/Adjustment%20of%20Status/I485_performancedata_fy2019_qtr2.csv"

with requests.Session() as s:
    # Use generator to speed up the process
    response = s.get(csv_url, stream=True)
    decoded_content = response.content.decode(
        "cp1252"
    )  # Could not decode utf-8, so windows codepage 1252 was required
    reader = csv.reader(decoded_content.splitlines(), delimiter=",")
    city_cases = []
    combined_categories = []
    us_state = list(map(str.lower, us_state))

    for row in reader:
        # row = next(reader)
        # removing leading and trailing white space
        row = list(map(str.strip, row))
        row = list(map(str.lower, row))  # create lower case
        if "family-based" in row:
            categories = row  # for green card category
            application_status = next(reader)  # for application status
            found = False  # flag
            current_name = ""
            value = ""
            for category, status in zip(categories, application_status):
                if category == "family-based":
                    current_name = category + ":"
                    found = True
                elif found == False:
                    pass

                elif found == True:
                    if category == "":
                        pass
                    else:
                        current_name = category + ":"
                value = current_name + status
                combined_categories.append(value)

        if "total" in row[0]:
            total_case_numbers = row
        if row[0] == "alabama":  # if initial state, alabama
            while row[1] != "vermont":  # if final city, vermont
                if (
                    row[0] != ""
                ):  # if the state column is not empty, meaning this line is state
                    state_name = row[0].title()  # grab the state name
                elif (
                    row[0] == ""
                ):  # if the state column is empty, meaning this line is city
                    row_with_state = row
                    row_with_state[
                        0
                    ] = state_name  # adding the state name to the initial part
                    city_cases.append(row_with_state)
                row = next(reader)
                row = list(
                    map(str.strip, row)
                )  # removing leading and trailing white space
                row = list(map(str.lower, row))  # create lower case

    # Adding nice headers
    combined_categories[0:3] = ["State", "City", "Abbreviation"]
    # Only need first 23 columns
    city_cases = np.array([np.array(x[0:23]) for x in city_cases])
    combined_categories = combined_categories[0:23]
    # pandas data frame for better organization
    df = pd.DataFrame(data=city_cases)
