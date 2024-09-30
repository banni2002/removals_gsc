from datetime import datetime
import sqlite3
import os
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
import json
import time
import configparser

print("LOADING config .......")

config = configparser.ConfigParser()
config.read('config/config.ini')

db_path = config.get('DATABASE', 'db_path')
interval_hours = int(config.getint('settings', 'interval_hour'))

google_api_json_folder = "google_api_json"

google_api_json_files = [os.path.join(google_api_json_folder, f) for f in os.listdir(google_api_json_folder) if os.path.isfile(os.path.join(google_api_json_folder, f)) and f.endswith(".json")]

dict_http = dict()
def create_http_request(cursor_api_key):
    global dict_http
    pos_api_key = str(cursor_api_key)
    if pos_api_key in dict_http:
        http = dict_http[pos_api_key]
    else:
        scopes = ['https://www.googleapis.com/auth/indexing']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(google_api_json_files[cursor_api_key], scopes=scopes)
        http = credentials.authorize(httplib2.Http())
        dict_http[pos_api_key] = http
    return http


def index_url(url):
    global cursor_api_key
    while True:
        if cursor_api_key < len(google_api_json_files):
            print("API KEY: ", google_api_json_files[cursor_api_key])
            http = create_http_request(cursor_api_key=cursor_api_key)
        else:
            print("All API keys are exhausted")
            return False
        
        ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
        
        content = {}
        content['url'] = url.strip()
        content['type'] = "URL_UPDATED"
        json_ctn = json.dumps(content)

        response, content = http.request(ENDPOINT, method="POST", body=json_ctn)

        result = json.loads(content.decode())

        if "error" in result:
            print("Error({} - {}): {}".format(result["error"]["code"], result["error"]["status"], result["error"]["message"]))
            # check if the error is about quota
            if result["error"]["status"] == "RESOURCE_EXHAUSTED":
                print("Quota exhausted, change to next API key")
                cursor_api_key += 1
            else:
                print(" DUNG CHUONG TRINH - VUI LONG CHECK LOG")                
                return False
        else:
            print("urlNotificationMetadata.url: {}".format(result["urlNotificationMetadata"]["url"]))
            print("urlNotificationMetadata.latestUpdate.url: {}".format(result["urlNotificationMetadata"]["latestUpdate"]["url"]))
            print("urlNotificationMetadata.latestUpdate.type: {}".format(result["urlNotificationMetadata"]["latestUpdate"]["type"]))
            print("urlNotificationMetadata.latestUpdate.notifyTime: {}".format(result["urlNotificationMetadata"]["latestUpdate"]["notifyTime"]))
            return True
    
cursor_api_key = 0

if __name__ == "__main__":
    while True:
        cursor_api_key = 0
        dict_http = dict()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Query the 'products' table
        # cursor.execute("SELECT COUNT(*) FROM products WHERE is_index='NOT' AND state is null")
        cursor.execute("SELECT COUNT(*) FROM products WHERE state = 'submitted'")
        count_start = cursor.fetchone()[0]
        # print("---> Total of products NOT INDEX: ", count_start)

        cursor.execute("SELECT * FROM products WHERE is_index='NOT' AND state is null ORDER BY total_order DESC")
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        rows_as_dict = [{columns[index]: value for index, value in enumerate(row)} for row in rows]
        for row in rows_as_dict:
            if row['product_url']:
                print("INDEX", row['product_id'], row['product_url'])
                submitted = index_url(url=row['product_url'])
                if submitted:
                    cursor.execute(f"UPDATE products SET state = 'submitted', submitted_at = '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' WHERE product_id = {row['product_id']}")
                    conn.commit()
                else:
                    break
        cursor.execute("SELECT COUNT(*) FROM products WHERE state = 'submitted'")
        count_end = cursor.fetchone()[0]
        print("---> Number of products submitted: ", count_end - count_start)
        print("---> Total of products submitted: ", count_end)
        conn.close()
        print(f"*** Waiting for {interval_hours} hours before submitting the next set of products ***")
        time.sleep(interval_hours * 60 * 60)

