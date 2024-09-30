# i want to submit the bing search results to the sqlite database
import requests
import sqlite3
import json
import os
import time
import configparser


config = configparser.ConfigParser()
config.read('config/config.ini')

db_path = config.get('DATABASE', 'db_path')
interval_hours = int(config.getint('settings', 'interval_hour'))


if __name__ == "__main__":
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Query the 'products' table
    cursor.execute("SELECT COUNT(*) FROM products WHERE is_index='NOT' AND state is null")
    count = cursor.fetchone()[0]
    print("---> Total of products NOT INDEX: ", count)

    cursor.execute("SELECT * FROM products WHERE is_index='NOT' AND state is null ORDER BY total_order DESC")
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    # iterate through each row in the table with dictionary
    # Iterate through each row in the table
    rows_as_dict = [{columns[index]: value for index, value in enumerate(row)} for row in rows]
    # Iterate through each row in the dictionary form
    domain = "teezapos.com"
    # url = "https://bing.com/IndexNow"
    url = "https://api.indexnow.org/IndexNow"
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
    }
    key = "f97a868712a649c59429108e42c34fe9"
    keyLocation = f"https://{domain}/{key}.txt"
    print(keyLocation)
    urlList = []
    counter = 0
    limitation = 10
    for row in rows_as_dict:
        counter += 1
        urlList.append(row['product_url'])
        if counter > limitation:
            break

    print(urlList)

    payload = {
        "host": domain,
        "key": key,
        "keyLocation": keyLocation,
        "urlList": urlList
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    print(response.status_code)
    print(response.text)

    print("FINISHED")