from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize the ChromeDriver
driver = webdriver.Chrome()

# Replace this with your actual URL
url = "how does a mini split work"

# Open the URL in the browser
driver.get(url)
driver.get('https://www.google.com/?gl=us')
# Find the div with jsname="NRdf4c"
div_element = driver.find_element(By.XPATH, '//div[@jsname="NRdf4c"]')

# Extract the URL from the div
url = div_element.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')

# Print the extracted URL
print("Extracted URL:", url)

# Close the browser
driver.quit()
