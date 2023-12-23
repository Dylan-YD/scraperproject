from django.conf import settings
import os
import csv
import time
import numpy as np
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from django.core.files.storage import default_storage
import boto3
from botocore.exceptions import NoCredentialsError
import io
import hashlib
import base64
from io import BytesIO


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
    last_screenshot_count = -1
    for sub_list in file_paths:
        
        if isinstance(sub_list, list):
            
            for file_path in sub_list:
                
                try:
                    screenshot_count = int(file_path.split("_")[-1].split(".")[0])
                    
                    if screenshot_count > last_screenshot_count:
                        last_screenshot_count = screenshot_count
                except (ValueError, AttributeError):
                    continue
    
    return last_screenshot_count


def upload_to_s3(image, s3_path):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    
    content_io = io.BytesIO()
    image.save(content_io, format="PNG")  # Adjust the format if your image is not in PNG format

    # Calculate Content-MD5
    content_md5 = base64.b64encode(hashlib.md5(content_io.getvalue()).digest()).decode('utf-8')

    print(content_md5)

    # Upload the content to S3 with Content-MD5
    s3.put_object(Body=content_io.getvalue(), Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=s3_path, ContentMD5=content_md5)





def scrape_google_ads(query, max_ads=4):
    """
    function to scrape google ads from google search results.

    Args:
        query (str): query to search for
    """

    indexes = []

    options = Options()
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service("/opt/homebrew/bin/chromedriver")
    scraper = webdriver.Chrome(service=service, options=options)
    scraper.set_window_size(2048, 1080)

    url = f"https://www.google.com/search?q={query}"
    
    scraper.get(url)

    full_page_path = f"media/data/{query}/full/full_page.png"
    
    try:
        # Capture screenshot as PNG byte stream
        screenshot_content = scraper.get_screenshot_as_png()

        initial_ads = scraper.find_elements(By.CSS_SELECTOR, ".uEierd")
      
        for i, element in enumerate(initial_ads):
            if i >= max_ads:
                break
            location = element.location
            size = element.size
            screenshot_content_copy = BytesIO(scraper.get_screenshot_as_png())

            try:
                im = Image.open(screenshot_content_copy)
                left = location["x"]
                top = location["y"]
                right = location["x"] + size["width"]
                bottom = location["y"] + size["height"]
                im = im.crop((left, top, right, bottom))
                # Rest of your code...
            except ValueError as ve:
                print(f"Error opening/cropping image for element {i}: {ve}")
                continue
            
            #last screenshot
            last_screenshot_count = get_last_screenshot_count(
                file_paths=default_storage.listdir(f"media/data/{query}/")
            )
            if not is_empty_image(im):
                s3_screenshot_path = f"media/data/{query}/{query}_{last_screenshot_count + 1}.png"
                upload_to_s3(im, s3_screenshot_path)                       
                indexes.append(last_screenshot_count+1)
            
            ads = []
            while True:
                scraper.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                time.sleep(3)
                new_ads = scraper.find_elements(By.CSS_SELECTOR, ".uEierd")
                if new_ads == ads or len(new_ads) >= max_ads:                    
                    break
                if new_ads:
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
                        
                        screenshot_content_copy = BytesIO(screenshot_content)

                        im = Image.open(screenshot_content_copy)
                        im = im.crop((left, top, right, bottom))

                        
                        if not is_empty_image(im):
                            s3_screenshot_path = f"media/data/{query}/{query}_{last_screenshot_count + 1}.png"
                            upload_to_s3(im, s3_screenshot_path)                            
                            indexes.append(last_screenshot_count+1)
                    

        
        descriptions = scraper.find_elements(By.CSS_SELECTOR, ".Va3FIb.r025kc.lVm3ye")
        
        desc = []
       
        for i, description in enumerate(descriptions):
            
            if i >= max_ads or i >= len(indexes):
                break
            data = description.text;#find_element(By.CSS_SELECTOR, "div").text.strip()
            
            desc.append(data)

        ad_containers = scraper.find_elements(By.CSS_SELECTOR, ".v5yQqb")
        
        
        ads = []
        for i, ad_container in enumerate(ad_containers):
            
            if i >= max_ads or i >= len(indexes):
                break
            
           
            url = ad_container.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            title = ad_container.find_element(By.CSS_SELECTOR, "div div div div div div").text.strip()
            ad = {
                "query": query,
                "title": title,
                "url": url,
                "description": desc[i],
                "screenshot": f"media/data/{query}/{query}_{indexes[i]}.png"
            }
            
            ads.append(ad)
        return ads
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"An error occurred: {e}")
        return []
    finally:
         scraper.quit()

def geotagging(query):
    url = f"https://www.google.com/search?q={query}"
    option = Options()
    option.add_argument("--headless")
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-dev-shm-usage")
    service = Service("/opt/homebrew/bin/chromedriver")
    scraper = webdriver.Chrome(service=service, options=option)
    
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
    finally:
        scraper.quit()

def save_ads_to_csv(ads):
    """
    Function to save ads to a CSV file.

    Args:
        ads (list): List of ads to save
    """

    header = ["query", "title", "url", "description", "contact_number", "company_board_members","company_email", "whois", "company_board_members_role", "secondary Contact","screenshot"]

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
