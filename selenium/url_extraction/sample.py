import requests
access_id = "mozscape-c62892296f"
secret_key = "f9ecf7cd7c3f361f4d529fb7f1797bf1"
url = "https://lsapi.seomoz.com/v2/url_metrics"
data = {
    "targets": ["best pellet stove"]
}
batch_size = 50
total_targets = 400
auth = (access_id, secret_key)

response = requests.post(url, json=data, auth=auth)

if response.status_code == 200:
    result = response.json()
    print(result)
else:
    print(f"Request failed with status code: {response.status_code}")