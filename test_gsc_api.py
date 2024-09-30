from google.oauth2 import service_account
from googleapiclient.discovery import build

# Đường dẫn đến file credentials JSON
KEY_FILE_LOCATION = 'google_api_json/gscteezapos@gsctoool.iam.gserviceaccount.com.json'

# Scopes cần thiết
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

# Tạo một credentials object từ file
credentials = service_account.Credentials.from_service_account_file(
        KEY_FILE_LOCATION, scopes=SCOPES)

# Tạo một service object cho Google Search Console
service = build('webmasters', 'v3', credentials=credentials)
# service = build('searchconsole', 'v1', credentials=credentials)

print(service.sites().list().execute())

site_url = 'sc-domain:teezapos.com'

# Lấy danh sách các vấn đề về lập chỉ mục
# response = service.urlInspection().index().inspect(
#     body={
#         "inspectionUrl": "https://teezapos.com/product/six-digits-code-shirt-nhentai-t-shirt/",
#         "siteUrl": site_url
#     }).execute()

# print(response)
# # Lọc và in ra danh sách các URL với issue "Discovered - currently not indexed"
# if 'indexStatusResult' in response:
#     for issue in response['indexStatusResult']['coverageState']:        
#         if issue == "Discovered - currently not indexed":
#             print(f"URL: {response['inspectionResult']['inspectedUrl']}, Issue: {issue}")


# Lấy danh sách các link đã index
start_date = '2023-01-01'
end_date = '2023-12-31'

# Tạo request body
next_page_token = None
request = {
    'startDate': start_date,
    'endDate': end_date,
    'dimensions': ['page'],
    'rowLimit': 100,
    # 'startRow': next_page_token,
    # 'searchType': 'web',
    'dimensionFilterGroups': [{
            'filters': [{
            'dimension': 'page',
            'operator': 'contains',
            'expression': 'Discovered - currently not indexed'
        }]
    }]
}

# Gọi API và lấy kết quả
response = service.searchanalytics().query(siteUrl=site_url, body=request).execute()

# In ra kết quả
count_not_index = 0
for row in response.get('rows', []):
    print(row)
    # print(row['keys'][0], row['clicks'], row['impressions'], row['ctr'], row['position'])
    exit()
    for issue in row['indexStatusResult']['coverageState']:
        if issue == "Discovered - currently not indexed":
            print(f"URL: {response['inspectionResult']['inspectedUrl']}, Issue: {issue}")
            count_not_index += 1

print("TOTAL Product", len(response.get('rows', [])))
print("TOTAL Product NOT INDEX", count_not_index)
print("FINISH!!!")