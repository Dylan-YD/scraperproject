import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from crawler.system.adscraper import scrape_google_ads, save_ads_to_csv

def whois_lookup (url):
    print("started whois lookup crawling...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service("path/to/chromedriver")
    scraper = webdriver.Chrome(service=service, options=options)
    scraper.set_window_size(2048, 1080)
    try:
        url = "https://www.whois.com/whois/" + url
        scraper.get(url)
        time.sleep(4)
        try:
            boards = scraper.find_elements(By.CLASS_NAME, "df-value")
            board_members = []
            for board in boards:
                try:
                    board_members.append(board.text)
                except:
                    pass
            print(board_members)
            return board_members[5]
        except:
            return ""
    except:
        return ""
    
def facebook_crawler(url):
    print("started facebook crawling...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service("path/to/chromedriver")
    scraper = webdriver.Chrome(service=service, options=options)
    scraper.set_window_size(2048, 1080)
    try:
        url = "https://www.google.com/search?q=" + "facebook page "+ url
        scraper.get(url)
        scraper.find_element(By.CLASS_NAME, "yuRUbf").click()
        time.sleep(4)
        scraper.find_element(By.CLASS_NAME,"x1i10hfl.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x1ypdohk.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x16tdsg8.x1hl2dhg.xggy1nq.x87ps6o.x1lku1pv.x1a2a7pz.x6s0dn4.x14yjl9h.xudhj91.x18nykt9.xww2gxu.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x78zum5.xl56j7k.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.xc9qbxq.x14qfxbe.x1qhmfi1").click()
        time.sleep(4)
        contact_number = scraper.find_elements(By.CLASS_NAME, "x193iq5w.xeuugli.x13faqbe.x1vvkbs.x10flsy6.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x4zkp8e.x41vudc.x6prxxf.xvq8zen.xo1l8bm.xzsf02u.x1yc453h")
        contact_list = []
        for contact in contact_number:
            try:
                contact_list.append(contact.text)
            except:
                contact_list.append("")
        return contact_list
    except:
        return ""

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
            try:
                details = facebook_crawler(url)
                ad["contact_number"] = details[1]
                email = details[2]
                ad["company_email"] = email
                print(details[1], details[2])
            except:
                ad["contact_number"] = ""
                ad["company_email"] = ""
            
            # try:
            #     whois = whois_lookup(url)
            #     print(whois)
            #     ad["whois"] = whois
            # except:
            ad["whois"] = ""

            ad["company_board_members_role"] = ""
            ad["company_board_members"] = ""

        except:
            return []
        
    save_ads_to_csv(ads)    
    print("ads saved to csv")
    return ads
