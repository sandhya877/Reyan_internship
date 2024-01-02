from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import requests
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pandas as pd
import logging
# Define the functions for each ETL step
logging.basicConfig(filename="logname.text",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
def scrape_google_data():
    
    # Add your code here
    proxies = {'http': 'http://palivela.srihari@gmail.com:reyandigital@us-wa.proxymesh.com:31280'}
    data = pd.read_excel("data.xlsx")
    all_top_10_urls = []
    main_keywords = ["best pellet stove", "best wood burning stove"]
    logging.info("Running Urban Planning")
    for keyword in main_keywords:
        urls_collected = 0
        urls_list = set()
        # Construct the Google search URL with the keyword and location parameter
        url = f"https://www.google.com/search?q={keyword}&gl=us"
    
        # Send the HTTP GET request using the proxy
        response = requests.get(url, proxies=proxies)
        soup = BeautifulSoup(response.text, 'html.parser')
    
        result_links1 = soup.find_all('a', attrs={'data-ved': True})
        
        for idx, link in enumerate(result_links1):
            h3_element = link.find('h3', class_='zBAuLc l97dzf')
            span_element = link.find('span', class_='rQMQod Xb5VRe')
            if span_element:
                # This link contains an h3 element, so you can extract the href
                href = link['href']
                if urls_collected == 0:
                    all_top_10_urls.append([keyword, urls_collected, href])
                    urls_collected += 1
            if h3_element:
                # This link contains an h3 element, so you can extract the href
                href = link['href']
                if urls_collected == 0:
                    all_top_10_urls.append([keyword, urls_collected, href])
                    urls_collected += 1
                else:
                    all_top_10_urls.append([" ", urls_collected, href])
                    urls_collected += 1
    
        df = pd.DataFrame(all_top_10_urls, columns=["keyword", "position", "url"])
        print(df)
        df.to_csv("urls4.csv", index=False)

def mozscape_data():
    access_id = "mozscape-c62892296f"
    secret_key = "f9ecf7cd7c3f361f4d529fb7f1797bf1"
    url = "https://lsapi.seomoz.com/v2/url_metrics"
    data = pd.read_csv("urls1.csv")
    data1 = data["url"]
    batch_size = 50
    total_targets = len(data)

    PA = []
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

    limit = min(len(PA), len(DA), len(data))

    PA_values = PA[:limit] + [np.nan] * (len(data) - limit)
    DA_values = DA[:limit] + [np.nan] * (len(data) - limit)

    data.insert(3, "PA", PA_values)
    data.insert(4, "DA", DA_values)

    data.to_csv('transformed_data.csv', index=False)

# Define the Airflow DAG
dag = DAG('etl_scraping_mozscape_dag',
          description='ETL Process with Web Scraping and Mozscape',
          schedule_interval=None,  # You can set a schedule if needed
          start_date=datetime(2023, 10, 27),  # Start date
          catchup=False)

# Define the PythonOperators for each step
scrape_google_data_task = PythonOperator(
    task_id='scrape_google_data',
    python_callable=scrape_google_data,
    dag=dag
)

mozscape_data_task = PythonOperator(
    task_id='mozscape_data',
    python_callable=mozscape_data,
    dag=dag
)

# Set up task dependencies
scrape_google_data_task >> mozscape_data_task

if __name__ == "__main__":
    dag.cli()
