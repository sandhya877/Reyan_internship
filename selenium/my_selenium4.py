from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Proxy configuration
proxy = "38.154.227.167:5868"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'--proxy-server=http://{proxy}')

# Initialize the Chrome WebDriver with proxy options
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get('https://www.google.com')
print(driver.title) 

# Find the search input element and enter your keyword
keyword = "hspf rating"  # Replace with your desired keyword
search_input = driver.find_element(By.NAME, 'body')
search_input.send_keys(keyword)
search_input.send_keys(Keys.RETURN)
driver.implicitly_wait(10)
# Extract and print the URLs of the top 10 search results
search_results = driver.find_elements(By.CSS_SELECTOR, "h3")
for idx, result in enumerate(search_results[:10], start=1):
    link = result.find_element(By.XPATH, "..").get_attribute("href")
    print(f"{idx}. {link}")
# Kill browser instance
driver.quit()
