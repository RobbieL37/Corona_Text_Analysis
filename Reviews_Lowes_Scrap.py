# Python project for review scraping of Lowes
# Creado por: Adelphi Students & Juan Monsalvo

# FOR Lowes
# ----------------------------------------------------------------------------------------------------------------------
# Libraries import
# ----------------------------------------------------------------------------------------------------------------------
import time
import random
import pandas as pd

import re
import json
import requests

from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
# ----------------------------------------------------------------------------------------------------------------------
# Function definition
# ----------------------------------------------------------------------------------------------------------------------
# random time function
def sec():
    # Function for random number
    time = random.randrange(10, 15)
    return time


def get_data_xpath(xpath):
    # Function to capture the text on a xpath root
    try:
        text = driver.find_element(By.XPATH, xpath).text
    except:
        text = ''
        pass

    return text

# ----------------------------------------------------------------------------------------------------------------------
# Configuration and Global Variables
# ----------------------------------------------------------------------------------------------------------------------
# Market place
market_place = 'lowes.com'

# Path for loading the URL sites
url_path_toilet = 'https://www.lowes.com/pd/Project-Source-Project-Source-Pro-Flush-2-Piece-Single-Flush-' \
                  'Elongated-Chair-Height-White-1-28-GPF/1003066162'

# url_path_toilet = 'https://www.lowes.com/pd/Project-Source-Project-Source-Danville-Single-Flush-12in-Rough-' \
#                   'In-2-Piece-Chair-Height-Elongated-Bowl-1-28-GPF-White/5000026209'
# url_path_toilet = 'https://www.lowes.com/pd/American-Standard-Mainstream-White-WaterSense-Elongated-Chair-Height-' \
#                   '2-Piece-Toilet-12-in-Rough-In-Size-ADA-Compliant/5001899855'
# url_path_toilet = 'https://www.lowes.com/pd/American-Standard-Saver-White-WaterSense-Labeled-Elongated-Chair-Height-' \
#                   '2-piece-Toilet-12-in-Rough-In-Size/3380314'
# url_path_toilet = 'https://www.lowes.com/pd/American-Standard-Colony-White-Elongated-Standard-Height-2-Piece-Toilet-' \
#                   '12-in-Rough-In-Size/50280511'
# url_path_toilet = 'https://www.lowes.com/pd/American-Standard-Mainstream-White-WaterSense-Round-Chair-Height-2-Piece-' \
#                   'Toilet-12-in-Rough-In-Size/3286026'


# Price information
currency = 'USD'
price = 119.0
# ----------------------------------------------------------------------------------------------------------------------
# Selenium
# ----------------------------------------------------------------------------------------------------------------------
# Configuration of Chrome
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')

# This
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument('--headless')
# options.add_argument("start-maximized")

# Setting the WebBrowser
s = Service(ChromeDriverManager().install())

# Loading the WebBrowser
driver = webdriver.Chrome(service=s, options=options)
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Main code
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Selenium and wait for the page to load
print('\n')
print(url_path_toilet)
driver.get(url_path_toilet)
time.sleep(sec())  # Random Wait between request

# ----------------------------------------------------------------------------------------------------------------------
# Product Information
# ----------------------------------------------------------------------------------------------------------------------
product_name = driver.find_element(By.XPATH, './/*[@id="pdp-lpd"]/div/div[1]/h1').text
sku = driver.find_element(By.XPATH, './/*[@id="pdp-lpd"]/div/div[2]/p[2]').text

print("Product Name:", product_name)
print("SKU:", sku)
print('\n')

# ----------------------------------------------------------------------------------------------------------------------
# Load Reviews Information
# ----------------------------------------------------------------------------------------------------------------------
# Click load review
load_review = driver.find_element(By.XPATH, './/*[@id="preview-reviews"]/div[2]/div/button')
load_review.click()
time.sleep(sec())  # Random Wait between request

# For loop for loading 10 more reviews
for i in range(1, 51):
    print(f'Click #{i}')
    readmore = driver.find_element(By.XPATH, '//*[@id="rrApp"]/div/div[2]/div/div/div[2]/div[' + str(6 + (i*10))
                                   + ']/button')
    readmore.click()
    time.sleep(sec())  # Random Wait between request

# ----------------------------------------------------------------------------------------------------------------------
# Read Reviews Information
# ----------------------------------------------------------------------------------------------------------------------
# Create a for loop to collect all the reviews
review_list = []
for i in range(6, 506):
    # Print to keep a track of the advance
    print(f'Scraping review #{i-5}')

    # Check and click the load more button
    try:
        time.sleep(sec())
        readmore = driver.find_element(By.XPATH, '//*[@id="rrApp"]/div/div[2]/div/div/div[2]/div[' + str(
            i) + ']/div[1]/div/div[1]/div/button')
        readmore.click()
    except:
        pass

    # Collect the items with XPATH
    subject = get_data_xpath(xpath='//*[@id="rrApp"]/div/div[2]/div/div/div[2]/div[' + str(i) +
                                   ']/div[1]/div/div[1]/div/p[1]')
    author = get_data_xpath(xpath='//*[@id="rrApp"]/div/div[2]/div/div/div[2]/div[' + str(i) +
                                  ']/div[1]/div/div[2]/div/span[1]')
    date = get_data_xpath(xpath='//*[@id="rrApp"]/div/div[2]/div/div/div[2]/div[' + str(i) +
                                ']/div[1]/div/div[2]/div/span[2]')
    review = get_data_xpath(xpath='//*[@id="rrApp"]/div/div[2]/div/div/div[2]/div[' + str(i) +
                                  ']/div[1]/div/div[1]/div/p[2]')
    stars = driver.find_element(By.XPATH, '//*[@id="rrApp"]/div/div[2]/div/div/div[2]/div[' + str(i) +
                                  ']/div[1]/div/div[1]/div/span/meta').get_attribute("content")

    # Save collected data on a list
    items = [market_place, url_path_toilet, product_name, sku, price, currency, subject, author, date, review, stars]
    review_list.append(items)

like_list = []
fbs = driver.find_elements(By.CLASS_NAME, 'review-row')
for fb in fbs:
    string = fb.find_element(By.CLASS_NAME, 'cgcfbbtncol').text
    like = string[(string.find('(', 0) + 1): (string.find(')', 0))]  # need to improve
    dislike = string[(string.find('(', 4) + 1): (string.find(')', 4))]  # need to improve

    # Saving in a list
    like_list.append([like, dislike])

# ----------------------------------------------------------------------------------------------------------------------
# Export to dataframe
# ----------------------------------------------------------------------------------------------------------------------
# Put the lists into dataframe
columns_name = ['Market_place', 'URL', 'Product_name', 'SKU', 'Price', 'Currency', 'Subject', 'Author', 'Date',
                'Review', 'Stars']
review_df = pd.DataFrame(data=review_list, columns=columns_name)
like_df = pd.DataFrame(data=like_list, columns=['like', 'dislike'])

# Mergin both data set
review_df = review_df.merge(like_df, left_index=True, right_index=True, how='left')

# ----------------------------------------------------------------------------------------------------------------------
# Export to .csv file
# ----------------------------------------------------------------------------------------------------------------------
review_df.to_csv('./XX_Reviews/' + market_place + '_' + url_path_toilet.split('/')[-1] + '.csv', index=False)
print(review_df)
