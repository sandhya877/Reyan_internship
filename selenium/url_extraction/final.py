import requests
import pandas as pd
import numpy as np

access_id = "mozscape-c62892296f"
secret_key = "f9ecf7cd7c3f361f4d529fb7f1797bf1"
url = "https://lsapi.seomoz.com/v2/url_metrics"
data = pd.read_excel("urls1.xlsx")
data1 = data["url"]
batch_size = 50
total_targets = len(data)
df = pd.read_csv('urls1.csv')  # Initialize the DataFrame outside the loop

PA = []  # Initialize PA and DA lists outside the loop
DA = []

for i in range(total_targets // batch_size):
    batch_start = i * batch_size
    batch_end = (i + 1) * batch_size
    data_batch = {
        "targets": data1[batch_start:batch_end].tolist()
    }
    auth = (access_id, secret_key)
    response = requests.post(url, json=data_batch, auth=auth)

    if response.status_code == 200:
        result = response.json()
        results = result.get("results", [])
        for res in results:
            page_authority = res.get("page_authority", "N/A")
            domain_authority = res.get("domain_authority", "N/A")
            PA.append(page_authority)
            DA.append(domain_authority)

# Calculate the limit once after all batches are processed
limit = min(len(PA), len(DA), len(df))

# Extend PA and DA lists with NaN values
PA_values = PA[:limit] + [np.nan] * (len(df) - limit)
DA_values = DA[:limit] + [np.nan] * (len(df) - limit)

# Insert PA and DA columns into the DataFrame
df.insert(3, "PA", PA_values)
df.insert(4, "DA", DA_values)

print(df.head(5))
