import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from crawler.system.adscraper import scrape_google_ads, save_ads_to_csv

def finding_company_boardmembers (url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service("path/to/chromedriver")
    scraper = webdriver.Chrome(service=service, options=options)
    scraper.set_window_size(2048, 1080)

    scraper.get(url)
    boards = scraper.find_elements(By.XPATH, "//*[contains(text(), 'Director') or contains(text(), 'Founder') or contains(text(), 'CEO') or contains(text(), 'Manager') or contains(text(), 'Owner') or contains(text(), 'Principal') or contains(text(), 'Partner') or contains(text(), 'Chairman') or contains(text(), 'President') or contains(text(), 'Vice President') or contains(text(), 'CFO') or contains(text(), 'CTO') or contains(text(), 'COO') or contains(text(), 'CIO') or contains(text(), 'CDO') or contains(text(), 'CMO') or contains(text(), 'CRO') or contains(text(), 'CPO') or contains(text(), 'CLO') or contains(text(), 'CBO') or contains(text(), 'CVO') or contains(text(), 'CISO') or contains(text(), 'CLO') or contains(text(), 'CDO') or contains(text(), 'CIO') or contains(text(), 'CFO') or contains(text(), 'CPO') or contains(text(), 'CVO') or contains(text(), 'CISO') or contains(text(), 'CLO') or contains(text(), 'CDO') or contains(text(), 'CIO') or contains(text(), 'CFO') or contains(text(), 'CPO') or contains(text(), 'CVO') or contains(text(), 'CISO')]")
    board_members = []
    for board in boards:
        try:
            text = board.get_attribute('innerText')
            board_mem = re.findall(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', text)
            board_members.append(board_mem)
        except:
            pass
    return board_members

def finding_company_contact_number(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service("path/to/chromedriver")
    scraper = webdriver.Chrome(service=service, options=options)
    scraper.set_window_size(2048, 1080)

    scraper.get(url)
    try:
        contact_elements = scraper.find_elements(By.XPATH, "//*[contains(text(), 'Contact') or contains(text(), 'Contact Us') or contains(text(), 'Contact Me') or contains(text(), 'Contact Information') or contains(text(), 'Contact Details') or contains(text(), 'Contact Info') or contains(text(), 'call us') or contains(text(), 'Call Us') or contains(text(), 'call') or contains(text(), 'telephone') or contains(text(), 'tel') or contains(text(), 'CALL') or contains(text(), 'tel:')]")
        
        contact_numbers = []
        for element in contact_elements:
            text = element.get_attribute('innerText')
            phone_numbers = re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text)
            contact_numbers.extend(phone_numbers)
        return contact_numbers
    except:
        return None

def finding_company_email(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        email = soup.find_all('a', href=re.compile(r'^mailto:'))
        email = email[0].get_text()
        return email
    except:
        return None

def finding_company_boardmembers_role(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        role = soup.find_all('a', href=re.compile(r'^mailto:'))
        role = role[0].get_text()
        return role
    except:
        return None

def url_content_scraper(query):
    option = Options()
    option.add_argument("--headless")
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-dev-shm-usage")
    service = Service("path/to/chromedriver")
    scraper = webdriver.Chrome(service=service, options=option)
    scraper.set_window_size(2048, 1080)

    ads = scrape_google_ads(query)
    if not ads:
        return []
    for ad in ads:
        url = ad["url"]
        print(url)
        try:
            url = scraper.find_element(By.XPATH, "//a[contains(text(), 'Contact Us'), contains(text(), 'Contact'), contains(text(), 'About'), contains(text(), 'About Us'), contains(text(), 'meet our team')]").click()
            contact_number = finding_company_contact_number(url)
            if contact_number:
                print(contact_number)
            company_email = finding_company_email(url)
            if company_email:
                print(company_email)
            url = scraper.find_element(By.XPATH, "//a[contains(text(), 'meet our team'), contains(text(), 'Meet Our Team') contains(text(), 'Our Team'), contains(text(), 'Our team'), contains(text(), 'our team'), contains(text(), 'Team'), contains(text(), 'team'), contains(text(), 'Board Members'), contains(text(), 'board members'), contains(text(), 'Board Member'), contains(text(), 'board member'), contains(text(), 'Board of Directors'), contains(text(), 'board of directors'), contains(text(), 'Board of Director'), contains(text(), 'board of director'), contains(text(), 'Contact')]").click()
            board_members = finding_company_boardmembers(url)
            if board_members:
                print(board_members)
            board_member_role = finding_company_boardmembers_role(url)
            if board_member_role:
                print(board_member_role)

            contact_number = finding_company_contact_number(url)
        
            ad["company_contact_number"] = contact_number[0]
            ad["company_board_members"] = board_members[0]
            ad["company_email"] = company_email
            ad["company_board_members_role"] = board_member_role

        except:
            ad["contact_number"] = "not found"
            ad["company_board_members"] = "not found"
            ad['company_email'] = "not found"
            ad["company_board_members_role"] = "not found"

    save_ads_to_csv(ads)    
    print("ads saved to csv")
    print(ads)
    return ads
