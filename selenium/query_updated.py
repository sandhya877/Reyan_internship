from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from urllib.parse import urlparse

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
# Set up your web driver (make sure you have the appropriate driver installed)
driver = webdriver.Chrome(options=chrome_options)  # For Chrome

# Create an empty DataFrame to store the search results
df = pd.DataFrame({"keyword": [],"position":[], "url": []})

# Read the list of keywords from your DataFrame
data = pd.read_excel("data.xlsx")
keywords = list(data["Main Keyword"])
url_set = set()  # Use a set to store unique URLs
result_list1 = []  # Change the variable name to result_list

# Navigate to the Google search page
driver.get("https://www.google.com/?gl=us")
original_target_values1 = []

# Iterate through the list of keywords
for keyword in keywords:
    search_box = driver.find_element(By.NAME, 'q')
    search_box.clear()
    search_box.send_keys(keyword)
    search_box.submit()

    # Wait for the search results to load (you may need to adjust the waiting time)
    time.sleep(5)  # Wait for 5 seconds (you can change this as needed)
    '''
    # Assuming you have already selected the div elements with the second XPath
    div_elements_2 = driver.find_elements(By.XPATH, '//block-component')

    # Extract and print the href attribute values using the second XPath
    for div_element in div_elements_2:
        anchor_elements = div_element.find_elements(By.XPATH, './/a[@data-ved]')
        for anchor_element in anchor_elements:
            href = anchor_element.get_attribute("href")
            parsed_url = urlparse(href)
            website_domain = f"{parsed_url.scheme}://{parsed_url.netloc}/"
            if website_domain not in url_set:
                url_set.add(website_domain)
                result_list.append([keyword, href])
                df = pd.DataFrame(result_list, columns=["keyword", "url"])
                print(href)
    
    # Assuming you have already selected the div elements with the first XPath

    div_elements_1 = driver.find_elements(By.XPATH, '//div[@data-hveid and @data-ved and contains(@style, "width:600px")]')
    print(keyword)
    # Extract and print the href attribute values using the first XPath
    for div_element in div_elements_1:
       
        anchor_elements = div_element.find_elements(By.XPATH, './/a[@data-ved]')
        for anchor_element in anchor_elements:
            href = anchor_element.get_attribute("href")
            parsed_url = urlparse(href)
            website_domain = f"{parsed_url.scheme}://{parsed_url.netloc}/"

            if website_domain not in url_set:
                print(website_domain)
                url_set.add(website_domain)
                result_list.append([keyword, href])
                df = pd.DataFrame(result_list, columns=["keyword", "url"])

    '''
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, 'search')))

    # Find the div elements matching the criteria
        # Assuming you have already selected the div elements
    #div_elements = driver.find_elements(By.XPATH, '//div[@data-hveid and @data-ved and contains(@style, "width:600px")]//span[@original_target]')

    #div_elements = driver.find_elements(By.XPATH, '//div[@class="kb0PBd cvP2Ce jGGQ5e" and @data-snhf]//a')
    #div_elements = driver.find_elements(By.XPATH, '//div[@class="kb0PBd cvP2Ce jGGQ5e" and @data-snf="x5WNvb"]//a[@jscontroller="M9mgyc"]')
    #div_elements = driver.find_elements(By.XPATH, '//a[@jsname="UWckNb" and @data-ved and @ping and @jscontroller="M9mgyc"]')
    #div_elements = driver.find_elements(By.XPATH, '//div[@jscontroller="SC7lYd" and @data-ved and contains(@style,"width:600px")]//a[@ping and @jsname="UWckNb" and @data-ved]')
    div_elements=driver.find_elements(By.XPATH,'//div[@class="yuRUbf"]//span/a')
    print(keyword)
    div_elements=div_elements[1]
    grandparent = div_elements.find_element(By.XPATH, './../../..')
    grandparent_class = grandparent.get_attribute("class")
    print(grandparent_class)
    '''
    for idx,div_element in enumerate(div_elements):
        original_target = div_element.get_attribute('href')
        print(original_target)
        original_target_values1.append([keyword,idx, original_target])
    
        
    # Create a DataFrame with the correct structure
    df = pd.DataFrame(original_target_values1, columns=["keyword","position","url"])

    df.to_csv("search_results2.csv", index=False)
driver.quit()
'''