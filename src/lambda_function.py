# coding: utf-8

import re
import json
from urllib import request
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials


WINDOWS_RELEASE_INFORMATION_URL = "https://winreleaseinfoprod.blob.core.windows.net/winreleaseinfoprod/en-US.html"
SPREADSHEET_ID = "12vLBLJXKzCuTHk4H8v2qjkY2A4mVTnsxwprxNBrYgrs"


def scraping(url):
    html = request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    table_elms = soup.find_all(id=re.compile('historyTable_*'))
    tables = {}

    for elm in table_elms:
        version = list(elm.previous_sibling.previous_sibling.strings)[1].split()[1]
        table = [["OS build", "Availability date", "Servicing option", "Kb number", "Kb article"]]

        tables[version] = table

        for tr in elm.find_all("tr"):
            td_elms = tr.find_all("td")

            if len(td_elms) < 4:
                continue

            table.append([
                    f"'{td_elms[0].string}",
                    f"=datevalue(\"{td_elms[1].string}\")",
                    "".join(list(td_elms[2].strings)),
                    td_elms[3].a and td_elms[3].string.split(" ")[1],
                    td_elms[3].a and td_elms[3].a.get("href")
            ])

    return tables


def sheets_service():
    creds = Credentials.from_service_account_file("credentials.json")
    return build("sheets", "v4", credentials=creds)


def write_table(service, spreadsheet_id, sheet_name, table):
    sheet = service.spreadsheets()

    range_ = f"{sheet_name}!A1:F{len(table) + 1}"
    try:
        sheet.values().get(spreadsheetId=spreadsheet_id, range=range_).execute()
    except:
        body = {
            "requests": {
                "addSheet": {
                    "properties": {
                        "title": sheet_name
                    }
                }
            }
        }
        sheet.batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

    body = {"values": table}
    option = "USER_ENTERED"
    request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=option, body=body)
    request.execute()


def lambda_handler(event, context):
    tables = scraping(WINDOWS_RELEASE_INFORMATION_URL)

    service = sheets_service()
    for version, table in tables.items():
        write_table(service, SPREADSHEET_ID, version, table)

    return
