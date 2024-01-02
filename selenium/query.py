from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
# Set up your web driver (make sure you have the appropriate driver installed)
driver = webdriver.Chrome()  # For Chrome
search_results_data = []
#df = pd.DataFrame({"Websites": []})
unique_links = set()
# Create an empty DataFrame to store the search results
df = pd.DataFrame({"keyword": [], "position": [], "url": []})
# Navigate to the Google search page
driver.get("https://www.google.com")

# Perform a search (replace 'your search query' with your actual query)
search_query = "how does a mini split work"

search_box = driver.find_element(By.NAME, 'q')
search_box.send_keys(search_query)
search_box.submit()

# Wait for the search results to load (you may need to adjust the waiting time)
time.sleep(5)  # Wait for 5 seconds (you can change this as needed)

# Find the 'h3' elements
# Use WebDriverWait to wait for the presence of at least one 'h3' element

# Assuming you have already selected the div elements with the desired attributes and stylediv_elements = driver.find_elements(By.XPATH, '//div[@data-hveid and @data-ved and contains(@style, "width:600px")]//a[@data-ved]')
# Assuming you have already selected the div elements with the desired attributes and style
# Assuming you have already selected the div elements with the desired attributes and style

# Use the provided XPath expression to find the elements
elements = driver.find_elements(By.XPATH, '//block-component')

# Extract and print the href attribute values

for div_element in elements:
    anchor_elements = div_element.find_elements(By.XPATH, './/a[@data-ved]')
    for anchor_element in anchor_elements:
        href = anchor_element.get_attribute("href")
        print(href)

div_elements = driver.find_elements(By.XPATH, '//div[@data-hveid and @data-ved and contains(@style, "width:600px")]')
for div_element in div_elements:
    anchor_elements = div_element.find_elements(By.XPATH, './/a')
    for anchor_element in anchor_elements:
        href = anchor_element.get_attribute("href")
        print(href)

# Loop through the 'h3' elements and get their parent 'div' elements
#for h3_element in h3_elements:
    #parent_div = h3_element.find_element(By.XPATH, "./ancestor::div")
    #print(parent_div.text)  # Print the text of the parent 'div' element

# Close the web driver when you're done
driver.quit()
