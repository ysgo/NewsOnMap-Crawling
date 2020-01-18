def startCrawling():
    from selenium import webdriver
    import pandas as pd
    import time, sys, re
    import pymysql
    from decouple import config

    startTime = time.time()
    connect = pymysql.connect(host=config('DB.URL'), port=int(config('DB.PORT')), user=config('DB.USER'),
                         passwd=config('DB.PASSWORD'), db=config('DB.NAME'), charset='utf8', autocommit=True)
    cursor = connect.cursor()

    # chromedriver version 79.0
    # chrome headless mode options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('lang=ko_KR')
    chrome_options.add_argument('--log-level=3')

    browser = webdriver.Chrome('chromedriver', chrome_options=chrome_options, service_log_path='NUL')
    browser.get('https://www.bigkinds.or.kr/v2/news/search.do')
    list_category=[]; list_newsname=[]; list_title=[]; list_date=[]; list_url=[]; list_content=[]; list_dataSize=[]
    print('getElementText is Start')
    try:
        for menu in range(4, 5):
            if menu == 4:
                menu = 6
            category_btn_link = '#filter-category-00' + str(menu) + '000000'
            category_btn = browser.find_element_by_css_selector(category_btn_link)
            category_btn.click()
            time.sleep(3)

            category_link = '#filter-category > div > div:nth-child(' + str(menu) + ') > label'
            category = browser.find_element_by_css_selector(category_link).text
            category = category[:2]

            page = 4
            for pageNB in range(1, 2):
                for i in range(1, 3):
                    print('pageNB : ' + str(pageNB))
                    print('i : ' + str(i))
                    newsname_link = '#news-results > div:nth-child(' + str(i) + ') > div.news-item__body > div.news-item__meta > a'
                    newsname = browser.find_element_by_css_selector(newsname_link).text

                    date_link = '#news-results > div:nth-child(' + str(i) + ') > div.news-item__body > div.news-item__meta > span.news-item__date'
                    date = browser.find_element_by_css_selector(date_link).text

                    title_link = '#news-results > div:nth-child(' + str(i) + ') > div.news-item__body > h4'
                    title_elm = browser.find_element_by_css_selector(title_link)
                    title = title_elm.text
                    title_elm.click()
                    time.sleep(2)

                    ## News Detail Modal Open ##
                    img_link = '#news-detail-modal > div > div > div.modal-body > div > div > img'

                    img_elm = browser.find_elements_by_css_selector(img_link)
                    url = str(0)
                    if len(img_elm) != 0:
                        url = img_elm[0].get_attribute('src')
                    content_link = '#news-detail-modal > div > div > div.modal-body > div'
                    content = browser.find_element_by_css_selector(content_link).text
                    content = re.sub('\n', '<br>', content)
                    time.sleep(2)

                    close_btn_link = '#news-detail-modal > div > div > div.modal-header > button > span'
                    close_btn = browser.find_element_by_css_selector(close_btn_link)
                    close_btn.click()
                    time.sleep(2)

                    dataSize = sys.getsizeof([category, newsname, title, date, url, content])

                    print('category : ' + category)
                    print('newsname : ' + newsname)
                    print('title : ' + title)
                    print('date : ' + date)
                    print('url : ' + url)
                    print('content : ' + content)
                    print('dataSize: ' + str(dataSize))

                    sql = "SELECT count(id) FROM news_lists WHERE title = %s AND data_size = %s"
                    cursor.execute(sql, (title, dataSize))
                    distinct_check = cursor.fetchone()[0]
                    if distinct_check > 0:
                        continue
                    else:
                        sql = "INSERT INTO news_lists (name, title, category, date, url, content, data_size) " \
                              "values (%s, %s, %s, %s, %s, %s, %s)"
                        cursor.execute(sql, (newsname, title, category, date, url, content, dataSize))

                    list_category.append(category)
                    list_newsname.append(newsname)
                    list_title.append(title)
                    list_date.append(date)
                    list_url.append(url)
                    list_content.append(content)
                    list_dataSize.append(dataSize)

                if page == 4:
                    break
                page_btn_link = '#news-results-pagination > ul > li:nth-child(' + str(page) + ') > a'
                page_btn = browser.find_element_by_css_selector(page_btn_link)
                page_btn.click()
                time.sleep(5)
                if page == 10:
                    page = 4
                else:
                    page += 1

            if menu == 6:
                break
            # browser.execute_script('scrollBy(0, 250);')
            # time.sleep(2)
            reset_btn_link = '#collapse-step-2 > div > div > div.col-sm-3.col-lg-2 > div > h4 > button > i'
            reset_btn = browser.find_element_by_css_selector(reset_btn_link)
            reset_btn.click()
            time.sleep(5)

        ## Dataframe by Pandas
        result_data = {
            'category': list_category,
            'newsname': list_newsname,
            'title': list_title,
            'date': list_date,
            'url': list_url,
            'content': list_content,
            'dataSize': list_dataSize
        }
        result = pd.DataFrame(result_data)
    except:
        print('exception interrupt')
        result = None
        pass # 예외 발생시 그냥 종료함. continue를 써야 다음 루프 진행
    else:
        print('getElement is Finish')
    finally:
        browser.quit()
        connect.commit()
        connect.close()
        endTime = time.time()
        print('StartTime : ' + str(startTime) + ', EndTime : ' + str(endTime))
        print('Total execution time estimate : ' + str(endTime - startTime))
    return result

