import os

from jpype import getDefaultJVMPath
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import time

from collections import Counter
from konlpy.tag import Okt

options = webdriver.ChromeOptions()

#자동꺼짐 방지
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

java_home = os.environ.get('JAVA_HOME')
jvm_path = getDefaultJVMPath()
if not jvm_path:
    jvm_path = f"{java_home}/bin/server/jvm.dll"
okt = Okt(jvmpath=jvm_path)

exclude_count_words = ['보이스피싱']
exclude_count_lengths = [1]
exclude_count_ranges = [(1, 3)]

# 설정 및 웹 페이지 열기
path = r"C:\Users\DU\Desktop\chromedriver.exe"
s = Service(path)
driver = webdriver.Chrome(options=chrome_options)



search_keywords = ['보이스피싱', '스미싱']
black_keywords = ['예방', 'AI', '시스템', '협약', '배상', '교육', '저출생', '육아', '수강', '영화']

def process_text(text):
    words = okt.nouns(text)  # 명사만 추출
    words = [
        word for word in words
        if word not in exclude_count_words and
        len(word) not in exclude_count_lengths
    ]
    return words


def sort_dict_by_value(d):
    return {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}


def infinite_to_end_scrolling():
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


def set_data_to_array_and_get_word_count():
    seen_titles = set()
    word_count_total = Counter()  # 모든 기사의 단어 출현 횟수를 누적할 Counter 객체
    for title, content in zip(titles, contents):
        if search_keyword in content.text:
            # black_keywords 중 하나라도 포함되면 해당 기사를 건너뜀
            if any(word in content.text for word in black_keywords) or any(
                    word in title.text for word in black_keywords):
                continue
                # 제목이 이미 처리된 적이 있는 경우 건너뜀
            if title.text in seen_titles:
                continue
            link = title.get_dom_attribute('href')

            words = process_text(content.text)
            word_count = Counter(words)
            word_count_total += word_count

            item = {
                'search_keyword': search_keyword,
                'title': title.text,
                'content': content.text,
                'link': link,
                # 'count': dict(word_count)
            }
            data.append(item)
            seen_titles.add(title.text)
    # 출현 횟수가 제외 범위에 속하는 단어를 필터링
    word_count_total = {
        word: count for word, count in word_count_total.items()
        if not any(start <= count <= end for start, end in exclude_count_ranges)
    }
    return word_count_total


for search_keyword in search_keywords:
    driver.get(f'https://search.naver.com/search.naver?where=news&query={search_keyword}&pd=4')
    driver.implicitly_wait(3)
    driver.maximize_window()
    infinite_to_end_scrolling()

    titles = driver.find_elements(By.CSS_SELECTOR, '.news_contents .news_tit')
    if not titles:
        continue
    contents = driver.find_elements(By.CSS_SELECTOR, '.news_dsc .dsc_wrap > a')
    data = []
    word_count_result = set_data_to_array_and_get_word_count()

    # word_count_total을 단어 출현 횟수 기준으로 내림차순 정렬
    sorted_word_count = sort_dict_by_value(dict(word_count_result))
    data.append(sorted_word_count)

    with open(f'news_phishing_{search_keyword}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

driver.close()
