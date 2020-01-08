from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# chromedriver version 79.0

# chrome headless mode options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('lang=ko_KR')
chrome_options.add_argument('--disable-logging')
# or '--log-level=3' to shut the logging

browser = webdriver.Chrome('chromedriver', chrome_options=chrome_options, service_log_path='NUL')
browser.implicitly_wait(2)

browser.get('https://www.bigkinds.or.kr/v2/news/search.do')

category = browser.find_element_by_xpath('//*[@id="filter-category"]/div/div[1]/label')
category_btn = browser.find_element_by_xpath('//*[@id="filter-category-001000000"]')
category_btn.click()

time.sleep(4)
newsname = browser.find_element_by_xpath('//*[@id="news-results"]/div[1]/div[2]/div[2]/a')
title_hrf = browser.find_element_by_xpath('//*[@id="news-results"]/div[1]/div[2]/h4')
title_hrf.click()

time.sleep(2)

title = browser.find_element_by_xpath('//*[@id="myModalLabel"]')
date = browser.find_element_by_xpath('//*[@id="news-detail-modal"]/div/div/div[1]/div[2]/span[4]')
author = browser.find_element_by_xpath('//*[@id="news-detail-modal"]/div/div/div[1]/div[2]/span[5]')
img_url = browser.find_element_by_xpath('//*[@id="news-detail-modal"]/div/div/div[2]/div/div/img')

contents = browser.find_element_by_xpath('//*[@id="news-detail-modal"]/div/div/div[2]/div')

time.sleep(2)

close_btn = browser.find_element_by_xpath('//*[@id="news-detail-modal"]/div/div/div[1]/button/span')
close_btn.click()

print(newsname.text)
print(category)
print(title)
print(date.text)
print(author)
print(contents.text)

browser.quit()