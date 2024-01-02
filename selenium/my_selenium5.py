from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from urllib.parse import urlparse
import time

# List of keywords to search for
keywords = [
    "how does a mini split work",
    "eer vs seer",
    "hspf rating",

]

data = pd.read_excel("data.xlsx")
data = list(data["Main Keyword"])

# Initialize the ChromeDriver
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Create a function to extract up to 10 unique URLs for a given keyword
def extract_urls_for_keyword(keyword):
    driver.get('https://www.google.com/?gl=us')

    # Find the search input element and enter the keyword
    search_input = driver.find_element(By.NAME, 'q')
    search_input.send_keys(keyword)
    search_input.send_keys(Keys.RETURN)
    driver.implicitly_wait(15)

    # Scroll down to load more results
    for _ in range(3):  # Adjust the number of scrolls as needed
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(2)  # Adjust the delay as needed

    # Extract up to 10 unique URLs
    search_results_data = []
    unique_links = set()
    search_results = driver.find_elements(By.XPATH, '//a[@jscontroller="M9mgyc"]')
    for idx, result in enumerate(search_results[5:]):
        link = result.get_attribute('href')
        parsed_url = urlparse(link)
        website_domain = f"{parsed_url.scheme}://{parsed_url.netloc}/"
        if website_domain not in unique_links:
            unique_links.add(link)
            if idx==0:
               search_results_data.append([keyword, idx , link])
            else:
                 search_results_data.append([" ", idx , link])
            if len(search_results_data) >= 10:
                break
    print(keyword, len(search_results_data))
    return search_results_data

# Initialize an empty DataFrame
df = pd.DataFrame(columns=["keyword", "position", "url"])

# Iterate through the list of keywords and extract URLs
for keyword in keywords:
    search_results_data = extract_urls_for_keyword(keyword)
    df = pd.concat([df, pd.DataFrame(search_results_data, columns=["keyword", "position", "url"])], ignore_index=True)

# Write all the data to a CSV file
df.to_csv("search_results1.csv", index=False)

# Close the browser
driver.quit()