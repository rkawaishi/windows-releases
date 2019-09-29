# coding: utf-8

import re
import json
from urllib import request
from bs4 import BeautifulSoup


WINDOWS_RELEASE_INFORMATION_URL = "https://winreleaseinfoprod.blob.core.windows.net/winreleaseinfoprod/en-US.html"


def scraping(url):
    html = request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    table_elms = soup.find_all(id=re.compile('historyTable_*'))
    tables = {}

    for elm in table_elms:
        version = list(elm.previous_sibling.previous_sibling.strings)[1].split()[1]
        table = []

        tables[version] = table

        for tr in elm.find_all("tr"):
            td_elms = tr.find_all("td")

            if len(td_elms) < 4:
                continue

            table.append([
                    td_elms[0].string,
                    td_elms[1].string,
                    td_elms[2].string,
                    td_elms[3].a and td_elms[3].string.split(" ")[1],
                    td_elms[3].a and td_elms[3].a.get("href")
            ])

    return tables


def lambda_handler(event, context):
    tables = scraping(WINDOWS_RELEASE_INFORMATION_URL)
    print(tables)
    return 'Test'
