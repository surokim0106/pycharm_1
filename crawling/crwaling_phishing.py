import selenium
from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import json
import pymysql


options = webdriver.ChromeOptions()
import time

#자동꺼짐 방지
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)


# 설정 및 웹 페이지 열기
path = r"C:\Users\DU\Desktop\chromedriver.exe"
s= Service(path)
driver = webdriver.Chrome(options = chrome_options)


search_keywords = ['보이스피싱', '스미싱', '신종사기']
black_keywords = ['예방','감사장','AI','시스템','협약','배상']


for search_keyword in search_keywords:
    driver.get(f'https://search.naver.com/search.naver?where=news&query={search_keyword}&pd=4')
    driver.implicitly_wait(3)
    driver.maximize_window()
    before_h = driver.execute_script("return window.scrollY")  # 스크롤 전 높이

    # 무한 스크롤(반복문) 모바일 페이지에서만 현재 정상 동작함(웹 페이지에서는 막힘)
    while True:
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)
        # 바디 태그 선택 후 끝까지 내림

        time.sleep(1)  # 스크롤 사이 페이지 로딩 시간 주기

        after_h = driver.execute_script("return window.scrollY")  # 스크롤 후 높이

        if after_h == before_h:
            break  # 더이상 내려갈 곳이 없기 때문에 무한루프를 탈출함.

        before_h = after_h

    titles = driver.find_elements(By.CSS_SELECTOR, '.news_contents > a:nth-child(2)')
    if not titles:
        continue
    contents = driver.find_elements(By.CSS_SELECTOR, '.news_dsc .dsc_wrap > a')
    data = []
    for title, content in zip(titles, contents):
        if str(content.text).find(search_keyword) != -1:
            for word in black_keywords:
                if str(content.text).find(word) != -1 or str(title.text).find(word) != -1:
                    break
                else:
                    link = title.get_dom_attribute('href')
                    item = {
                        'search_keyword': search_keyword,
                        'title': title.text,
                        'content': content.text,
                        'link': link
                    }
                    data.append(item)
                    break
    inner_title = ''
    new_data = []
    for item in data:
        if inner_title == item['title']:
            new_data.append(item)
            break
        else:
            inner_title = item['title']
    with open(f'news_phishing_{search_keyword}.json', 'w', encoding='utf-8') as f :
        json.dump(new_data, f,ensure_ascii = False, indent = 4)

driver.close()
