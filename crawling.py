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
id=None; newsname=None; title=None; category=None; date=None; url=None; content=None; dataSize=None
print('getElementText is Start')
try:
    for menu in range(4, 5):
        if menu == 4:
            menu = 6
        category_btn_link = '#filter-category-00' + str(menu) + '000000'
        print(category_btn_link)
        print(menu)
        category_btn = browser.find_element_by_css_selector(category_btn_link)
        category_btn.click()

        category_link = '#filter-category > div > div:nth-child(' + str(menu) + ') > label'
        category = browser.find_element_by_css_selector(category_link).text
        category = category[:2]
        print(category)

        page = 4
        for pageNB in range(1, 2):
            for i in range(1, 2):
                print(pageNB);print(i)
                newsname_link = '#news-results > div:nth-child(' + str(i) + ') > div.news-item__body > div.news-item__meta > a'
                newsname = browser.find_element_by_css_selector(newsname_link).text
                print(newsname)

                date_link = '#news-results > div:nth-child(' + str(i) + ') > div.news-item__body > div.news-item__meta > span.news-item__date'
                date = browser.find_element_by_css_selector(date_link).text
                print(date)

                title_link =  '#news-results > div:nth-child(' + str(i) + ') > div.news-item__body > h4'
                title_elm = browser.find_element_by_css_selector(title_link)
                title = title_elm.text
                print(title)
                title_elm.click()

                ## News Detail Modal Open ##
except:
    print('d')
else:
    print('e')
finally:
    print('z')

browser.quit()