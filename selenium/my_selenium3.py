from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from urllib.parse import urlparse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


# List of keywords to search for
keywords = [
    "how does a mini split work",
    "eer vs seer",
    "hspf rating",
    "is 72°C ideal temperature for air conditioning",
    "increase airflow to one room",
    
]
data=pd.read_excel("data.xlsx")
data=list(data["Main Keyword"])
# Initialize the ChromeDriver
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
search_results_data = []
#df = pd.DataFrame({"Websites": []})
unique_links = set()
# Create an empty DataFrame to store the search results
df = pd.DataFrame({"keyword": [], "position": [], "url": []})


for keyword in keywords:
    driver.get('https://www.google.com/?gl=us')
        # $x('//div[@data-hveid and @data-ved and contains(@style, "width:600px")]')
    try:
        # Find the search input element and wait for it to be present and clickable
        search_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'q')))
        search_input.send_keys(keyword)
        search_input.send_keys(Keys.RETURN)
    except NoSuchElementException:
        print("Search input element not found. Check the page structure or your locator.")
    # Use explicit wait to wait for search results
    #WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3")))

        
    div_elements = driver.find_elements(By.XPATH, '//div[@jsname="NRdf4c"]')

    for div_element in div_elements:
        url = div_element.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        print("Extracted URL:", url)


    '''
    # Extract and print the URLs of the top 10 search results
    search_results = driver.find_elements(By.CSS_SELECTOR, "h3")
    
    for idx, result in enumerate(search_results[:10], start=1):
        link = result.find_element(By.XPATH, '//div[@data-hveid and @data-ved and contains(@style, "width:600px")]').get_attribute("href")
        print(link)
        
        parsed_url = urlparse(link)
        website_domain = f"{parsed_url.scheme}://{parsed_url.netloc}/"
        if website_domain not in unique_links:
            unique_links.add(link)
            if idx == 1:
                search_results_data.append([keyword,idx, link])
            else:
                search_results_data.append([ " ",idx, link])
        # Create a DataFrame from the collected data
    df = pd.DataFrame(search_results_data, columns=["keyword", "position", "url"])
    df.to_csv("search_results1.csv", index=False)
        #if link not in df["url"].tolist():
            #new_row = pd.DataFrame([{"keyword": keyword, "position": idx, "url": link}])
            #df = pd.concat([df, new_row], ignore_index=True)
    # Close the browser after processing each keyword

# Save the DataFrame to a CSV file

driver.quit()



        # Append the search results data to the DataFrame
        # Save the DataFrame to a new Excel sheet
#with pd.ExcelWriter("websites.xlsx", engine="xlsxwriter") as writer:
    #df.to_excel(writer, sheet_name="Websites", index=False)
'''