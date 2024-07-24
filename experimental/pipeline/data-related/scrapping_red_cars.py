import time
import os
import requests
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path  # this will get you the path variable

# Setup Chrome service with the correct path
service = Service(executable_path=binary_path)

# Set up Selenium WebDriver
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode
# service = Service(executable_path='path_to_your_chromedriver')  # Replace with your ChromeDriver path
driver = webdriver.Chrome(service=service, options=chrome_options)


# Function to scroll down the page
def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # Function to download image


def download_image(url, folder_path, count):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img.save(os.path.join(folder_path, f"red_car_{count}.jpg"))
    except Exception as e:
        print(f"Could not download {url} - {e}")


# Open Google Images
driver.get("https://images.google.com/")
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("real red car")
search_box.send_keys(Keys.RETURN)

# Scroll down to load more images
for _ in range(5):
    scroll_down(driver)

# Find image elements
image_elements = driver.find_elements(By.CSS_SELECTOR, "img[id^='dimg']")

# Create folder to save images
folder_path = "red_cars"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Download images
count = 0
for img in image_elements:
    try:
        # Try to get the 'src' attribute first, if it's not present, get 'data-src'
        src = img.get_attribute("src")
        if not src:
            src = img.get_attribute("data-src")
        if src and "http" in src:
            download_image(src, folder_path, count)
            count += 1
    except Exception as e:
        print(f"Error with image {count}: {e}")

# Close the browser
driver.quit()

print(f"Downloaded {count} images of red cars.")