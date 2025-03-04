import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
from PIL import Image
import requests
import os
from dotenv import load_dotenv
from selenium.common.exceptions import StaleElementReferenceException

load_dotenv()
chrome_profile_path = os.getenv("chrome_profile_path")

chrome_options = Options()
chrome_options.add_argument(chrome_profile_path) 
chrome_options.add_argument("--disable-application-cache")
# chrome_options.add_argument("--headless")

driver = uc.Chrome(options=chrome_options)
def generate_image(text,path):
    driver.get("https://x.com/i/grok")
    WebDriverWait(driver, 10).until(
    lambda d: d.execute_script("return document.readyState") == "complete"
)
    textarea = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((By.XPATH, "//*[@placeholder='Ask anything']"))
    )

    # textarea = driver.find_element(By.XPATH, "//*[@placeholder='Ask anything']")


    try:
        textarea.send_keys(text)
        textarea.send_keys(Keys.RETURN)
    except StaleElementReferenceException:
        print("Element became stale after input, but ignoring since input succeeded.")
    time.sleep(30)

    image_elements = driver.find_elements(By.TAG_NAME, "img")
    for i in image_elements:
        print(i.get_attribute("src"))

    # Check if there are images available
    if image_elements:
        first_image = image_elements[2]  # Get the first image
        image_url = first_image.get_attribute("src")  # Extract its URL
        driver.get(image_url)
        print("went to the creation page")
        screenshot_path = os.path.join(os.getcwd(), f"comics_generated/{path}.png")
        cropped_path = os.path.join(os.getcwd(), "cropped_screenshot.png")
        time.sleep(2)
        driver.save_screenshot(screenshot_path)

        # # Download and save the image
        # if image_url:
        #     image_data = requests.get(image_url).content
        #     image_path = os.path.join(os.getcwd(), "first_image_1.jpg")
        #     with open(image_path, "wb") as file:
        #         file.write(image_data)
        #     print(f"First image saved at {image_path}")
        # else:
        #     print("Failed to extract image URL.")
    else:
        print("No images found on the page.")
generate_image("Generate an image for this prompt: The city starts to return to normal. People cheer for Spiderman and Ironman..","page_3_panel_1")

