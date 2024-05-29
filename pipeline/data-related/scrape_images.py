import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

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
    "Toyota cars", "Honda cars", "Ford cars", "Chevrolet cars", "BMW cars", "Mercedes-Benz cars", "Audi cars", 
    "Lexus cars", "Nissan cars", "Hyundai cars", "Kia cars", "Volkswagen cars", "Volvo cars", "Tesla cars", 
    "Subaru cars", "Mazda cars", "Jeep cars", "Chrysler cars", "Land Rover cars", "Ferrari cars", "Porsche cars", 
    "Lamborghini cars", "Bugatti cars", "Bentley cars", "Maserati cars", "Rolls-Royce cars", "Aston Martin cars", 
    "McLaren cars", "Alfa Romeo cars", "Jaguar cars", "Fiat cars", "Mini cars", "Infiniti cars", "Acura cars", 
    "Genesis cars", "Lincoln cars", "Buick cars", "Cadillac cars", "GMC cars", "Ram cars", "Smart cars"
]

# Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # To run Chrome in headless mode
chrome_options.add_argument("--no-proxy-server")

# Chrome WebDriver path
webdriver_path = "D:\chromedriver-win64\chromedriver.exe"  

# Create a directory to save images
folder_name = "scraped_images"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Set the limit of images to save
limit = 50

# Define a minimum width and height threshold for images (adjust as needed)
MIN_WIDTH = 150
MIN_HEIGHT = 150

# Initialize Chrome WebDriver
service = Service(webdriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

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
                        # Send a GET request to download the image
                        response = requests.get(image_url)
                        if response.status_code == 200 and response.content:  # Check if response content is not empty
                            # Save image locally
                            image_path = os.path.join(folder_name, f"{search_term.replace(' ', '_')}_{count}.jpg")
                            with open(image_path, 'wb') as img_file:
                                img_file.write(response.content)
                            print(f"Image {count + 1} of {search_term} saved successfully.")
                            count += 1
                            if count >= limit:
                                break
            except Exception as e:
                pass


finally:
    # Close WebDriver
    driver.quit()
