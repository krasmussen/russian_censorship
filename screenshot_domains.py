#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests
import json
import socket
import random

# Shorten socket timeout so we don't wait forever on stuff that doesn't exist anymore
socket.setdefaulttimeout(5)

blocked_pages = requests.get('https://reestr.rublacklist.net/api/v2/domains/json/')
blocked_pages_json = blocked_pages.json()
#with open('./6-28-data.json', 'r') as F:
#    blocked_pages_json = json.load(F)


# Set path Selenium (Downloaded previously)
CHROMEDRIVER_PATH = './chromedriver'
s = Service(CHROMEDRIVER_PATH)
WINDOW_SIZE = "1440,900"

# Options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(service=s, options=chrome_options)
driver.implicitly_wait(10)

# Randomize as I have ran this a few times and would prefer to see new sites hit into my screenshots directory first
random.shuffle(blocked_pages_json)

# Load each page and take a screenshot
for page in blocked_pages_json:
    domain = page.replace('*.', '')
    try:
        socket.gethostbyname(domain)
    except Exception as E:
        continue
    page = 'http://' + page
    try:
        driver.get(page)
        driver.get_screenshot_as_file("./screenshots/%s.png" %(domain))
        print(driver.title)
        print('got page %s' %(page))
    except Exception as E:
        pass
        #print('Failed to get page %s' %(page))
driver.close()
