# Python project for review scraping of Lowes
# Creado por: Adelphi Students & Juan Monsalvo

# FOR Home Depot
# ----------------------------------------------------------------------------------------------------------------------
# Libraries import
# ----------------------------------------------------------------------------------------------------------------------
import time
import random
import pandas as pd

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


def get_data_xpath(driver, xpath):
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
market_place = 'homedepot.com'

# Path for loading the URL sites
# url_path_toilet = 'https://www.homedepot.com/p/Glacier-Bay-2-Piece-1-28-GPF-High-Efficiency-Single-Flush-Elongated-' \
#                   'Toilet-in-White-N2428E/204074796'

url_path_toilet = 'https://www.homedepot.com/p/American-Standard-Reliant-2-piece-1-28-GPF-Single-Flush-Elongated-' \
                  'Toilet-in-White-Seat-Included-773CA101-020/319247071'

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
product_name = driver.find_element(By.XPATH, './/*[@id="root"]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/'
                                             'span/h1').text
''
sku = driver.find_element(By.XPATH, './/*[@id="root"]/div/div[2]/div[2]/div/div/h2[3]').text.split('#')[-1]

print("Product Name:", product_name)
print("SKU:", sku)
print('\n')

# Price information
currency = 'USD'

# Collecting the current price
price_raw = int(driver.find_element(By.XPATH, '//*[@id="eco-rebate-price"]/div[1]/div[2]/span[2]').text.strip())
decimals = float(driver.find_element(By.XPATH, '//*[@id="eco-rebate-price"]/div[1]/div[2]/span[3]').text.strip())
price = price_raw + (decimals / 100)

# ----------------------------------------------------------------------------------------------------------------------
# Read Reviews Information
# ----------------------------------------------------------------------------------------------------------------------
# Loading the reviews pages
# List to save the data
review_list = []

for j in range(1, 3):
    url_divide = url_path_toilet.split('/p/')
    url_path_toilet_review = url_divide[0] + '/p/reviews/' + url_divide[-1]

    driver.get(url_path_toilet_review + '/' + str(j))
    time.sleep(sec())  # Random Wait between request

    # Scrolling down to load the reviews
    driver.execute_script("window.scrollTo(0, 800)")
    time.sleep(sec())  # Random Wait between request

    # Create a for loop to collect all the reviews from the page
    for i in range(6, 36):
        # Print to keep a track of the advance
        print(f'Scraping review #{i-5}')

        # Collect the items with XPATH
        subject = get_data_xpath(driver=driver, xpath='//*[@id="ratings-and-reviews"]/div[' + str(i) +
                                       ']/div[1]/div[1]/div[2]/div/div/span')
        author = get_data_xpath(driver=driver, xpath='//*[@id="ratings-and-reviews"]/div[' + str(i) +
                                      ']/div[1]/div[1]/div[2]/div/div/div[2]/button')
        date = get_data_xpath(driver=driver, xpath='//*[@id="ratings-and-reviews"]/div[' + str(i) +
                                      ']/div[1]/div[1]/div[1]/div/span')
        review = get_data_xpath(driver=driver, xpath='//*[@id="ratings-and-reviews"]/div[' + str(i) +
                                       ']/div[1]/div[1]/div[2]/div/div/div[1]')
        stars = driver.find_element(By.XPATH, './/*[@id="ratings-and-reviews"]/div[' + str(i) +
                                    ']/div[1]/div[1]/div[1]/div/div/span').get_attribute("style").split(' ')[-1]

        # Converting the style info in a number of stars
        if stars == '20%;':
            stars = 1
        elif stars == '40%;':
            stars = 2
        elif stars == '60%;':
            stars = 3
        elif stars == '80%;':
            stars = 4
        elif stars == '100%;':
            stars = 5
        else:
            stars = 0

        # Save collected data on a list
        items = [market_place, url_path_toilet, product_name, sku, price, currency, subject, author, date, review, stars]
        review_list.append(items)

# ----------------------------------------------------------------------------------------------------------------------
# Export to dataframe
# ----------------------------------------------------------------------------------------------------------------------
# Put the lists into dataframe
columns_name = ['Market_place', 'URL', 'Product_name', 'SKU', 'Price', 'Currency', 'Subject', 'Author', 'Date',
                'Review', 'Stars']
review_df = pd.DataFrame(data=review_list, columns=columns_name)
# like_df = pd.DataFrame(data=like_list, columns=['like', 'dislike'])

# Mergin both data set
# review_df = review_df.merge(like_df, left_index=True, right_index=True, how='left')

# ----------------------------------------------------------------------------------------------------------------------
# Export to .csv file
# ----------------------------------------------------------------------------------------------------------------------
review_df.to_csv('./XX_Reviews/' + market_place + '_' + url_path_toilet.split('/')[-1] + '.csv', index=False)
print(review_df)
