import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import csv
import pandas as pd
sitemap_urls = [
    'https://www.electronicshub.org/post-sitemap.xml',
'https://www.electronicshub.org/post-sitemap.xml'	,
'https://www.electronicshub.org/post-sitemap2.xml',	
'https://www.electronicshub.org/post-sitemap3.xml',	
'https://www.electronicshub.org/post-sitemap4.xml',
'https://www.electronicshub.org/post-sitemap5.xml',
'https://www.electronicshub.org/page-sitemap.xml'
]
data_list=[]
# Iterate through the sitemap URLs and extract table data
for sitemap_url in sitemap_urls:

  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

  response = requests.get(sitemap_url, headers=headers)

  if response.status_code == 200:
            sitemap = BeautifulSoup(response.text, 'html.parser')
            xml_data = str(sitemap)
            root = ET.fromstring(xml_data)
            for element in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
              url = element.text
              data_list.append({'url': url})

# Create a DataFrame from the list of data
df = pd.DataFrame(data_list)

# Write all the data to a CSV file
df.to_csv("search_results1.csv", index=False)