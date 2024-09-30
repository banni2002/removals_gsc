
import requests


APP_ID = "cli_a6e198bee2785010"
APP_SECRET = "rbPJGP1FBLe5HEjI2K9Uze3WfZx7Mkpn"

ACCESS_TOKEN =  "t-g2066djjW7X2VB3IQD5TY2NIXYR3EYTLM25EXHBO"

sheet_token = "LzVyskwUNhhvyXtv873lnBt4gue"
sheet_id = "rUC156"
if __name__ == "__main__":
    #get tenant_access_token
    if not ACCESS_TOKEN:
        url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "app_id": APP_ID,
            "app_secret": APP_SECRET
        }
        response = requests.post(url, headers=headers, json=data)
        tenant_access_token = response.json()["tenant_access_token"]
        print("tenant_access_token: ", tenant_access_token)
        print("expire: ", response.json()["expire"])

    url = "https://open.larksuite.com/open-apis/sheets/v3/spreadsheets/LzVyskwUNhhvyXtv873lnBt4gue/sheets/query"
    payload = ''


    headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
