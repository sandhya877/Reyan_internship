import scrapy
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process
import pandas as pd

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
def run_spider(urls):
    urls = urls.tolist()  # Convert the Series to a list
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Your User Agent Here',
    })
    process.crawl(MySpider, urls=urls)
    process.start()


def run_multiprocessing():
    # List of URLs to scrape
    url_list = data["url"]

    # Specify the number of parallel processes
    num_processes = 5  # You can adjust this as needed

    # Create and start processes
    processes = []
    for i in range(num_processes):
        urls_chunk = url_list[i::num_processes]
        process = Process(target=run_spider, args=(urls_chunk,))
        process.start()
        processes.append(process)

    # Wait for all processes to finish
    for process in processes:
        process.join()

if __name__ == '__main__':
    run_multiprocessing()
