

#목표1: 서비스를 검색하여 부정적인 반응 추출 (서비스별, 네이버지식인 > 구글창 > 네이버카페) -> 셀레니움
#목표2: 피싱 관련 뉴스 기사 제목 + 내용 추출 (네이버뉴스, 다움뉴스) -> 스크래피 ->일단 불러오기 -> 데이터 필터링 -> 디비 저장
#목표3: 피싱 관련 키워드 추출 (네이버, 트위터) -> 스크래피 ->일단 불러오기 -> 데이터 필터링 -> 디비 저장

#데이터유니버스, 스마트피싱보호, 휴대폰분실보호, 오토콜, 휴대폰가족보호
#네이버카페 -> 로그인 클릭 통해서 쓸지 또는 다른 방법(로그인용 Api)

import selenium
from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver import ActionChains as AC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import json
import pymysql


options = webdriver.ChromeOptions()
import time
from time import sleep
import re


#자동꺼짐 방지
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)


# 설정 및 웹 페이지 열기
path = r"C:\Users\DU\Desktop\chromedriver.exe"
s= Service(path)
driver = webdriver.Chrome(options = chrome_options)
#데이터유니버스, 스마트피싱보호, 휴대폰분실보호, 오토콜, 휴대폰가족보호
search_keywords = ['데이터유니버스', '스마트피싱보호', '휴대폰분실보호', '오토콜', '휴대폰가족보호']

#conn = pymysql.connect(host= '디비호스트정보(ip)', user='id', password='password', db='schima이름', charset='utf8',
                #port= 3306)
#concursor = conn.cursor()

for search_keyword in search_keywords:
    driver.get(f"https://kin.naver.com/search/list.nhn?sort=none&section=kin&query={search_keyword}&period=1m")
    driver.implicitly_wait(3)

    titles = driver.find_elements(By.CSS_SELECTOR, '.basic1 li ._searchListTitleAnchor')
    if not titles:
        continue
    dates = driver.find_elements(By.CSS_SELECTOR, '.txt_inline')
    contents = driver.find_elements(By.CSS_SELECTOR, '.basic1 li dl dd:nth-child(3)')
    data = []
    for title, date, content in zip(titles, dates, contents):
        if str(content.text).find(search_keyword) != -1:
            link = title.get_dom_attribute('href')
           #concursor.execute('insert into titletable (title,link) values(%s,%s)', title.text,link )
            item = {
                'search_keyword': search_keyword,
                'title': title.text,
                'date': date.text,
                'content': content.text,
                'link': link
            }
            data.append(item)
    with open(f'crwaling_{search_keyword}.json', 'w', encoding='utf-8') as f :
        json.dump(data, f,ensure_ascii = False, indent = 4)


#driver.close()















#driver.find_element(By.NAME, "query").send_keys("스마트피싱보호")
#findbutton = driver.find_element(By.CSS_SELECTOR, "button.btn_search")
#findbutton.click()
#jisikbutton = driver.find_element(By.XPATH, '//*[@id="lnb"]/div[1]/div/div[1]/div/div[1]/div[1]/a')
#jisikbutton.click()
#optionbutton = driver.find_element(By.XPATH, '//*[@id="snb"]/div[1]/div/div[2]/a')
#optionbutton.click()
#onemonthbutton = driver.find_element(By.XPATH,'//*[@id="snb"]/div[2]/ul/li[1]/div/div[1]/a[5]')
#onemonthbutton.click()





















