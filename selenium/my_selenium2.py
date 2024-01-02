from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from seleniumwire import webdriver as wiredriver
PROXY_HOST = '38.154.227.167'
PROXY_PORT = '5868'

chrome_options = Options()
chrome_options.add_argument('--proxy-server=http://{}:{}'.format(PROXY_HOST, PROXY_PORT))

driver = wiredriver.Chrome(options=chrome_options)
keyword = "how does a mini split work"
driver.get("https://www.google.com")

search_box = driver.find_element_by_name("a")
search_box.send_keys(keyword)
search_box.submit()
# Wait for the search results to load
driver.implicitly_wait(10)

# Extract and print the URLs of the top 10 search results
search_results = driver.find_elements_by_css_selector("h3")
for idx, result in enumerate(search_results[:10], start=1):
    link = result.find_element_by_xpath("..").get_attribute("href")
    print(f"{idx}. {link}")

# Close the WebDriver when done
driver.quit()
