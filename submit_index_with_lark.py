from helper_ggsheet import get_array_ggsheets
from datetime import datetime
import configparser


print("LOADING config .......")

# read config file config.ini and get the values, using configparser 
config = configparser.ConfigParser()
config.read('config.ini')
# get the values from the config file
SHEET_ID = config['google_sheets_config']['sheet_id']
SHEET_DATA = config['google_sheets_config']['sheet_data']
COLUMN_NAME_STATUS = config['google_sheets_config']['column_name_status']
STATUS_PENDING = config['google_sheets_config']['status_pending']
STATUS_DONE = config['google_sheets_config']['status_done']


with open("main_google_api_config.txt", "r") as f:
    text = f.read().strip()
main_google_api_json = eval(text)

"/Users/tranthien/Documents/2.DATA/SEO/teezapos.com/teezapos.db3"
if __name__ == "__main__":
    sheet, sheet_rows, POSITION_COLUMN = get_array_ggsheets(sheet_id=SHEET_ID, sheet_name=SHEET_DATA, ggsheet_config_json=main_google_api_json)
    row_number = 0
    first_row = True
    sellers = []
    for sheet_row in sheet_rows:
        row_number += 1
        print("row number", row_number)
        if row_number <= 1:
            first_row = False
            continue
        
        state = sheet_row[POSITION_COLUMN[COLUMN_NAME_STATUS]]
        if state == STATUS_DONE:
            continue

        product_link = sheet_row[POSITION_COLUMN["product_url"]] 
        account = sheet_row[POSITION_COLUMN["Account"]]
        account_cookie = sheet_row[POSITION_COLUMN["Cookie"]]
        account_proxy = sheet_row[POSITION_COLUMN["Proxy"]]
    
