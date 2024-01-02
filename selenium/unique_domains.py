import pandas as pd
from urllib.parse import urlparse
import re
import requests
import numpy as np
import time

access_id = "mozscape-c62892296f"
secret_key = "f9ecf7cd7c3f361f4d529fb7f1797bf1"
url_main = "https://lsapi.seomoz.com/v2/url_metrics"

data = pd.read_csv("urls1.csv")
data = data["url"]
domains = set()
urls_list = []
for url in data:
    input_string = url

    url_pattern = r'https?://\S+'
    match = re.search(url_pattern, input_string)
    if match:
        url = match.group()
        urls_list.append(url)
        parsed_url = urlparse(url)
        website_domain = f"{parsed_url.scheme}://{parsed_url.netloc}/"
        if website_domain not in domains:
            domains.add(website_domain)

batch_size = 50
total_targets = len(data)

for i in range(total_targets // batch_size):
    batch_start = i * batch_size
    batch_end = (i + 1) * batch_size
    data = {
        "targets": urls_list[batch_start:batch_end]
    }
    auth = (access_id, secret_key)
    response = requests.post(url_main, json=data, auth=auth)
    if response.status_code == 200:
        try:
            result = response.json()
            df = pd.read_csv('urls1.csv')
            results = result.get("results", [])
            PA = []
            DA = []
            for res in results:
                page_authority = res.get("page_authority", "N/A")
                domain_authority = res.get("domain_authority", "N/A")
                PA.append(page_authority)
                DA.append(domain_authority)
            limit = min(len(PA), len(DA), len(df))

            PA_values = PA[:limit] + [np.nan] * (len(df) - limit)
            DA_values = DA[:limit] + [np.nan] * (len(df) - limit)

            df.insert(3, "PA", PA_values)
            df.insert(4, "DA", DA_values)
            df.to_csv('updated_urls2.csv', index=False)
            
            print("DataFrame saved to updated_urls1.csv")
            print(len(PA_values))
        except Exception as e:
            print(f"Error processing JSON response: {str(e)}")
    else:
        print(f"Request failed with status code: {response.status_code}")
    
    time.sleep(10)