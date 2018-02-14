from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re

driver = webdriver.Chrome()

driver.get("https://www.sephora.com/shop/lips-makeup?pageSize=300")


csv_file = open('lip1.csv', 'w')
writer = csv.writer(csv_file)
index = 1
prev_button = None


current_button = None
while True:
    try:
        if prev_button is not None:
            WebDriverWait(driver, 10).until(EC.staleness_of(prev_button))

        print("Scraping Page number " + str(index))
        index = index + 1
        time.sleep(3)

        products = driver.find_elements_by_xpath('//div[@class="css-115paux"]')

        print(len(products))
        print('='*50)
    
        for product in products:
            product_dict = {}
            driver.execute_script("arguments[0].scrollIntoView();", product)

            brand = product.find_element_by_xpath('.//span[@class="css-1r6no3d OneLinkNoTx"]').text
            name= product.find_element_by_xpath('.//span[@data-at="sku_item_name"]').text
            price = product.find_element_by_xpath('.//span[@data-at="sku_item_price_list"]').text
            prices = price.split('-')
            if len(prices) == 1:
                low_price = high_price = re.search('\d+', prices[0]).group()
            else:
                low_price = re.search('\d+', prices[0]).group()
                high_price = re.search('\d+', prices[1]).group()

            rate = product.find_element_by_xpath('.//div[@class="css-dtomnp"]').get_attribute('style')
            try:
                rate = re.search('\d+.\d+', rate).group()
            except:
                rate = ''

            link = product.find_element_by_xpath('./a').get_attribute('href')
            # Opens a new tab
            driver.execute_script("window.open()")

            # Switch to the newly opened tab
            driver.switch_to.window(driver.window_handles[1])

            # Navigate to new URL in new tab
            driver.get(link)
            try:
                reviews = driver.find_element_by_xpath('//span[@class="css-1dz7b4e"]').text
                reviews = re.search('\d+', reviews).group()
            except:
                reviews = ""

            try:
                likes = driver.find_element_by_xpath('//span[@class="css-9i5033"]').text
            except:
            	likes = ""

            # Close current tab
            driver.close()

            # Switch back to original tab
            driver.switch_to.window(driver.window_handles[0])

            product_dict['brand'] = brand
            product_dict['name'] = name
            product_dict['low_price'] = low_price
            product_dict['high_price'] = high_price
            product_dict['rate'] = rate
            product_dict['reviews'] = reviews
            product_dict['likes'] = likes
            print(product_dict)

            writer.writerow(product_dict.values())

        wait_button = WebDriverWait(driver, 10)
        current_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,
                                    '//div[@data-comp="Paginator"]/button[last()]')))
        prev_button = current_button
        current_button.click()
    except Exception as e:
        print(e)
        csv_file.close()
        driver.close()
        break  