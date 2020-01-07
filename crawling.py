from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# chromedriver version 79.0
browser = webdriver.Chrome('chromedriver')
browser.implicitly_wait(2)

browser.get('https://www.bigkinds.or.kr/v2/news/search.do')

menu_btn = browser.find_element_by_css_selector('#collapse-step-2 > div > div > div.col-sm-9.col-lg-10 > div.row > div.col-xs-12.col-lg-8.col-sm-8 > ul > li.active > a')
name = browser.find_element(By.XPATH, '/html/body/div[9]/div/h1')

print(menu_btn.text)
print(name.text)

time.sleep(1)
browser.quit()