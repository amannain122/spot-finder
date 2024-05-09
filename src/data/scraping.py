import os
import requests
from selenium import webdriver

# Initialize a browser driver (e.g., Chrome)
driver = webdriver.Chrome()

# Navigate to the website
driver.get("https://driving-tests.org/beginner-drivers/how-to-park-a-car-between-two-cars/#google_vignette")

# Find all image elements on the page
images = driver.find_elements_by_tag_name("img")

# Specify the folder to save the images
save_folder = "D:\spot-finder\data"

# Download and save each image
for i, img in enumerate(images):
    image_url = img.get_attribute("src")
    if image_url:
        image_filename = os.path.join(save_folder, f"image_{i}.jpg")
        with open(image_filename, "wb") as f:
            f.write(requests.get(image_url).content)
        print(f"Downloaded: {image_filename}")

# Close the browser
driver.quit()
