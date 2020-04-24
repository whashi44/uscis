
from os.path import basename
import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
"""
This code automatically download all the csv file from uscis website
"""

os.chdir("csv_deposit")
emp = ""
base = "https://www.uscis.gov/tools/reports-studies/immigration-forms-data?topic_id=20658&field_native_doc_issue_date_value%5Bvalue%5D%5Bmonth%5D=&field_native_doc_issue_date_value_1%5Bvalue%5D%5Byear%5D=&combined=&items_per_page=100"
with requests.Session() as s:
    url = s.get(base, stream=True).text
    soup = BeautifulSoup(url, "html.parser")
    # a = soup.select("a[href$='.csv']")
    for link in (urljoin(emp, a["href"]) for a in soup.select("a[href$='.csv']")):
        with open(basename(link), "wb") as write_file:
            write_file.write(requests.get(link).content)
