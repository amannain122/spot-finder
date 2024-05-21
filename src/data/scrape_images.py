from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import urllib.request
from aws import s3, s3_bucket_name
import io

# Function to scroll to the bottom of the page
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# List of search terms
search_terms = [
    "Toyota cars",
    "Honda cars",
    "Ford cars",
    "Chevrolet cars",
    "BMW cars",
    "Mercedes-Benz cars",
    "Audi cars",
    "Lexus cars",
    "Nissan cars",
    "Hyundai cars",
    "Kia cars",
    "Volkswagen cars",
    "Volvo cars",
    "Tesla cars",
    "Subaru cars",
    "Mazda cars",
    "Jeep cars",
    "Chrysler cars",
    "Land Rover cars",
    "Ferrari cars",
    "Porsche cars",
    "Lamborghini cars",
    "Bugatti cars",
    "Bentley cars",
    "Maserati cars",
    "Rolls-Royce cars",
    "Aston Martin cars",
    "McLaren cars",
    "Alfa Romeo cars",
    "Jaguar cars",
    "Fiat cars",
    "Mini cars",
    "Infiniti cars",
    "Acura cars",
    "Genesis cars",
    "Lincoln cars",
    "Buick cars",
    "Cadillac cars",
    "GMC cars",
    "Ram cars",
    "Smart cars"
]

# Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # To run Chrome in headless mode
chrome_options.add_argument("--no-proxy-server")

# Chrome WebDriver path
webdriver_path = "D:\\chromedriver_win32\\chromedriver"

# Create a directory to save images
folder_name = "scraped_images"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Set the limit of images to save
limit = 5

# Define a minimum width and height threshold for images (adjust as needed)
MIN_WIDTH = 150
MIN_HEIGHT = 150

# Initialize Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    for search_term in search_terms:
        # URL of Google Images with search term
        url = f"https://www.google.com/search?q={search_term}&source=lnms&tbm=isch"
        driver.get(url)

        # Scroll to the bottom of the page to load more images
        scroll_to_bottom(driver)

        # Find image elements
        image_elements = driver.find_elements(By.CSS_SELECTOR, "img")

        count = 0
        for i, image_element in enumerate(image_elements):
            try:
                # Get image dimensions
                width = int(image_element.get_attribute("width") or 0)
                height = int(image_element.get_attribute("height") or 0)

                # Check if image dimensions meet the threshold
                if width >= MIN_WIDTH and height >= MIN_HEIGHT:
                    image_url = image_element.get_attribute("src")
                    if image_url is not None:
                        # Read image data
                        image_data = urllib.request.urlopen(image_url).read()
                        # Wrap image data in a file-like object
                        image_fileobj = io.BytesIO(image_data)
                        # Define the object key with folder structure
                        image_key = f"{folder_name}/{search_term.replace(' ', '_')}_{count}.jpg"
                        # Upload the image to S3
                        s3.upload_fileobj(image_fileobj, s3_bucket_name, image_key)
                        print(f"Image {count + 1} of {search_term} uploaded to S3 successfully.")
                        count += 1
                        if count >= limit:
                            break
            except Exception as e:
                print(f"Error uploading image to S3 for {search_term}: {e}")

finally:
    # Close WebDriver
    driver.quit()
