import scrapy
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process
import pandas as pd
import requests
import random
import time
import datetime
import re

data = pd.read_excel("list.xlsx")

class MySpider(scrapy.Spider):
    name = 'my_spider'

    def __init__(self, urls=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = urls  # Pass the list of URLs to the spider

    def parse(self, response):
        url = response.url
        published_date = response.css('CSS_SELECTOR_FOR_PUBLISHED_DATE::text').get()
        edit_date = response.css('CSS_SELECTOR_FOR_EDIT_DATE::text').get()
        asin = response.css('CSS_SELECTOR_FOR_ASIN::text').get()

        yield {
            'URL': url,
            'Published Date': published_date,
            'Edit Date': edit_date,
            'ASIN': asin
        }


def run_spider(urls, output_csv):
    urls = urls.tolist()  # Convert the Series to a list
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Your User Agent Here',
    })

    # A list to store the results
    results = []

    # Iterate over the URLs
    for url in urls:
        url_data = {'url': url, 'ASIN': None, 'full_links': []}
        try:
            user_agents_list = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                # Add more user agents as needed
            ]
            time.sleep(random.randint(0, 2))
            response = requests.get(url, headers={"User-Agent": random.choice(user_agents_list)})
            affiliate_links = extract_specific_domain_links(response.text, "amzn")
            url_data['full_links'] = [unshorten_url(link) for link in set(affiliate_links)]
            asin_ids = [get_asin_id_from_url(link) for link in url_data['full_links']]
            asin_ids = [asin_id for asin_id in asin_ids if asin_id]
            url_data['asin_id'] = asin_ids

            for asin_id in asin_ids:
                results.append({'url': url, 'asin_id': asin_id})

        except Exception as e:
            print(f"ASIN failed for URL: {url}")
            print(f"Exception: {e}")
            continue

    results_df = pd.DataFrame(results)
    results_df.to_csv(output_csv, index=False)

    # Store the data in a database table
    current_date = datetime.datetime.now().strftime('%Y%m%d')
    table_name = f"url_asin_info_{current_date}"
    saved_table = create_table_from_csv(output_csv, table_name)

    print(f"Data saved to {output_csv} and {saved_table}")


def extract_specific_domain_links(text, domain):
    # Use a regular expression to extract all links from the text
    links = re.findall(r'https?://' + re.escape(domain) + r'[^\s]*', text)
    return links


def unshorten_url(url):
    session = requests.Session()  # so connections are recycled
    response = session.head(url, allow_redirects=True)
    return response.url


def get_asin_id_from_url(url):
    """ Given the Amazon URL, this function extracts the ASIN from
    Sample url: 'https://www.amazon.com/dp/B01M5DY5C8/ref=sr_1_1?keywords=kindle&qid=1568593042&sr=8-1'
    """
    # Use a regular expression to extract the ASIN from the URL
    try:
        asin = re.search(r'dp/(\w{10})(/|\?)', url).group(1)
        print(f'ASIN for URL {url}: {asin}')
        return asin
    except:
        print(f"ASIN failed for URL: {url}")
        return ""


def run_multiprocessing(input_csv_path, output_csv_path):
    # List of URLs to scrape
    url_list = data["url"]

    # Specify the number of parallel processes
    num_processes = 5  # You can adjust this as needed

    # Split URLs into chunks for multiprocessing
    url_chunks = [url_list[i::num_processes] for i in range(num_processes)]

    # Create and start processes
    processes = []
    for i, url_chunk in enumerate(url_chunks):
        output_file = f"{output_csv_path}_{i}.csv"
        process = Process(target=run_spider, args=(url_chunk, output_file))
        process.start()
        processes.append(process)

    # Wait for all processes to finish
    for process in processes:
         process.join()

    # Merge the results from multiple output files
    merged_results = pd.concat([pd.read_csv(f"{output_csv_path}_{i}.csv") for i in range(num_processes)])
    merged_results.to_csv(output_csv_path, index=False)


if __name__ == '__main__':
    input_csv_path = "list.xlsx"
    output_csv_path = "url_asin_september.xlsx"
    run_multiprocessing(input_csv_path, output_csv_path)
       
