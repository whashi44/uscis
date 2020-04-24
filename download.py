
from os.path import basename
import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
"""
This code automatically download all the csv file from uscis website
"""
path = "raw"
try:
    print(f"Making folder: {path}")
    os.mkdir(path)
except FileExistsError:
    pass
finally:
    os.chdir(path)
    print(f"Changed directory to: {path}")


base = "https://www.uscis.gov/tools/reports-studies/immigration-forms-data?topic_id=20658&field_native_doc_issue_date_value%5Bvalue%5D%5Bmonth%5D=&field_native_doc_issue_date_value_1%5Bvalue%5D%5Byear%5D=&combined=&items_per_page=100"
with requests.Session() as s:
    # stream will make it generator and parse faster
    url = s.get(base, stream=True).text
    # Specifying the parse is necessary to avoid warning
    soup = BeautifulSoup(url, "html.parser")
    # creating generator with all the url that end with .csv
    # the soup.select will include other unnecessary html parameter, hence urljoin is used to extract just the href
    for link in (urljoin("", a["href"]) for a in soup.select("a[href$='.csv']")):
        with open(basename(link), "wb") as write_file:
            print(f"saving .csv file:{link} to path")
            write_file.write(requests.get(link).content)
