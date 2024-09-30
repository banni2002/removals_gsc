import random
import traceback
import sys
import os
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from ggsheet_config_tranthien import GGSHEET_JSON_CONFIG as GGSHEET_JSON_CONFIG
import time
from datetime import datetime, timedelta


def get_dict_ggsheets(sheet_id, sheet_name, ggsheet_config_json={}):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    ggsheet_config_json = ggsheet_config_json if ggsheet_config_json else GGSHEET_JSON_CONFIG
    creds = ServiceAccountCredentials.from_json_keyfile_dict(ggsheet_config_json, scope)
    gc = gspread.authorize(creds)
    spreadsheet_id = sheet_id
    sheet_name = sheet_name
    wks = gc.open_by_key(spreadsheet_id)
    worksheet = wks.worksheet(sheet_name)
    records = worksheet.get_all_records()

    return records


def get_array_ggsheets(sheet_id, sheet_name, ggsheet_config_json={}):
    position_column = {}
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    ggsheet_config_json = ggsheet_config_json if ggsheet_config_json else GGSHEET_JSON_CONFIG
    creds = ServiceAccountCredentials.from_json_keyfile_dict(ggsheet_config_json, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(sheet_id)
    sheet = spreadsheet.worksheet(sheet_name)
    sheet_rows = sheet.get_all_values()
    row_number = 0
    first_row = True
    for sheet_row in sheet_rows:
        row_number += 1
        if first_row:
            first_row = False
            expected_headers = sheet_row
            for index, header in enumerate(expected_headers):
                position_column[header] = index
            break
    return sheet, sheet_rows, position_column


def write_ggsheet(row_number, pair_column_value, POSITION_COLUMN, sheet):
    running = True
    while running:
        try:
            cells = []
            for column, value in pair_column_value.items():
                cell = sheet.cell(row_number, POSITION_COLUMN[column] + 1)
                cell.value = value
                cells.append(cell)
            sheet.update_cells(cells)
            running = False
        except gspread.exceptions.APIError as sheet_error:
            if "Quota exceeded for quota" in str(sheet_error):
                print("Quota exceeded for quota Write Google sheet")
                time.sleep(70)
        except Exception as sheet_any_error:
            return False
    return True


def write_ggsheet_cells(row_number, pair_column_value, POSITION_COLUMN, sheet):
    for column, value in pair_column_value.items():
        while True:
            try:
                sheet.update_cell(row_number, POSITION_COLUMN[column] + 1, value)
                time.sleep(random.randint(1, 5))
                break
            except gspread.exceptions.APIError as sheet_error:
                if "Quota exceeded for quota" in str(sheet_error):
                    # print(traceback.print_exc())
                    print("Quota exceeded for quota Write Google sheet")
                    time.sleep(60)
    return True


def check_expired_date():
    current_date = datetime.now()
    start_date = datetime(2023, 10, 30)
    expiry_date = start_date + timedelta(days=90)

    if current_date <= expiry_date:
        return True
    else:
        print("Ứng dụng đã hết hạn sử dụng, vui lòng liên hệ New moon Company.")
        return False


def resource_path(relative_path):
    # return os.path.join(relative_path)
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

