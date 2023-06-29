
import os
import csv
import time
import numpy as np
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def is_empty_image(image):
    """
    Function to check if an image is empty.
    """
    grayscale_image = image.convert('L')
    pixels = np.array(grayscale_image)
    intensity_mean = np.mean(pixels)
    threshold = 10
    return intensity_mean < threshold

def get_last_screenshot_count(file_paths):
    # print(file_paths)
    last_screenshot_count = -1
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        try:
            screenshot_count = int(file_name.split("_")[-1].split(".")[0])
            if screenshot_count > last_screenshot_count:
                last_screenshot_count = screenshot_count
        except ValueError:
            continue
    return last_screenshot_count

def scrape_google_ads(query, max_ads=4):
    """
    function to scrape google ads from google search results.

    Args:
        query (str): query to search for
    """

    indexes = []

    os.makedirs(f"media/data/{query}", exist_ok=True)
    if os.path.exists(f"media/data/{query}"):
        pass
    else:
        os.makedirs(f"media/data/{query}", exist_ok=True)

    os.makedirs(f"media/data/{query}/full", exist_ok=True)
    if os.path.exists(f"media/data/{query}/full"):
        pass
    else:
        os.makedirs(f"media/data/{query}/full", exist_ok=True)

    # Set up selenium webdriver
    options = Options()
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service("path/to/chromedriver")
    scraper = webdriver.Chrome(service=service, options=options)
    scraper.set_window_size(2048, 1080)

    url = f"https://www.google.com/search?q={query}"
    scraper.get(url)
    time.sleep(2)
    try:
        # saving full image screenshot
        scraper.save_screenshot(f"media/data/{query}/full/full_page.png")
        initial_ads = scraper.find_elements(By.CSS_SELECTOR, ".uEierd")

        # screenshot_count = 0
        # saving individual ads only 4 items
        for i, element in enumerate(initial_ads):
            if i >= max_ads:
                break

            location = element.location
            size = element.size
            im = Image.open(f"media/data/{query}/full/full_page.png")
            left = location["x"]
            top = location["y"]
            right = location["x"] + size["width"]
            bottom = location["y"] + size["height"]

            im = im.crop((left, top, right, bottom))
            
            #last screenshot
            last_screenshot_count = get_last_screenshot_count(
                file_paths=os.listdir(f"media/data/{query}/")
            )
            if not is_empty_image(im):
                im.save(f"media/data/{query}/{query}_{last_screenshot_count+1}.png")
                indexes.append(last_screenshot_count+1)
            
            ads = []
            while True:
                scraper.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                time.sleep(3)
                new_ads = scraper.find_elements(By.CSS_SELECTOR, ".uEierd")
                if new_ads == ads or len(new_ads) >= max_ads:
                    break
                else:
                    ads = new_ads
                    for i, element in enumerate(ads):
                        if i >= max_ads:
                            break

                        location = element.location
                        size = element.size
                        left = location["x"]
                        top = location["y"]
                        right = location["x"] + size["width"]
                        bottom = location["y"] + size["height"]

                        im = im.crop((left, top, right, bottom))
                        if not is_empty_image(im):
                            im.save(f"media/data/{query}/{query}_{last_screenshot_count+1}.png")
                            indexes.append(last_screenshot_count+1)
        try:
            descriptions = scraper.find_elements(By.CSS_SELECTOR, ".MUxGbd.yDYNvb.lyLwlc")
            desc = []
            for i, description in enumerate(descriptions):
                if i >= max_ads:
                    break
                data = description.find_element(By.CSS_SELECTOR, "div").text.strip()
                desc.append(data)
        except:
            return desc.append("No description available")

        ad_containers = scraper.find_elements(By.CSS_SELECTOR, ".v5yQqb")
        ads = []
        for i, ad_container in enumerate(ad_containers):
            if i >= max_ads:
                break
            url = ad_container.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            title = ad_container.find_element(By.CSS_SELECTOR, "div div div div div div").text.strip()
            ad = {
                # "ad_id": ad_id,
                "query": query,
                "title": title,
                "url": url,
                "description": desc[i],
                "screenshot": f"media/data/{query}/{query}_{indexes[i]}.png"
            }
            ads.append(ad)
        scraper.quit()
        return ads
    except:
        return []
    

def geotagging(query):
    url = f"https://www.google.com/search?q={query}"
    scraper = webdriver.Chrome()
    scraper.set_window_size(2048, 1080)
    scraper.get(url)
    time.sleep(2)
    query_list_geo = []
    try:
        scraper.find_element(By.CLASS_NAME, "HzHK1").click()
        time.sleep(2)
        if scraper.find_element(By.CLASS_NAME, "QjCHvc").text.strip() == "No results found":
            return []
        first_geo = scraper.find_elements(By.CLASS_NAME, "QjCHvc")
        for i, geo in enumerate(first_geo):
            if i >= 4:
                break
            q = geo.find_element(By.TAG_NAME, "a").get_attribute("data-query")
            query_list_geo.append(q)
        return query_list_geo
    except:
        return [query]

def save_ads_to_csv(ads):
    """
    Function to save ads to a CSV file.

    Args:
        ads (list): List of ads to save
    """

    header = ["query", "title", "url", "description", "contact_number", "company_board_members","company_email", "company_board_members_role","screenshot"]

    if not os.path.exists("ads.csv"):
        with open("ads.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)

    existing_data = []

    with open("ads.csv", "r") as f:
        reader = csv.DictReader(f)
        existing_data = [(row['url'],row['title']) for row in reader]

    new_ads = []

    for ad in ads:
        if existing_data == []:
            new_ads.append(ad)
        else:
            if ad['url'] not in [data[0] for data in existing_data] and ad['title'] not in [data[1] for data in existing_data]:
                new_ads.append(ad)

    if new_ads:
        with open("ads.csv", "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writerows(new_ads)
