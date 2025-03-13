import os
import json
import time
import warnings
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from utils.utils import new_session, running_min, dict_ott
warnings.filterwarnings('ignore')


def get_path(relative_path):
    BASE_DIR = os.path.abspath(os.path.dirname(__file__)) 
    return os.path.normpath(os.path.join(BASE_DIR, relative_path)) 


def load_user_key():
    user_email = input('왓챠피디아 ID : ')
    with open(get_path("data/user/user_info.json"), "r") as f:
        user_info = json.load(f)
    user_key = user_info[user_email]

    return user_key


def scrape_wishes(driver, user_key):
    """유저의 '보고싶어요' 목록 접근"""
    
    # driver = webdriver.Chrome()
    
    url = f'https://pedia.watcha.com/ko-KR/users/{user_key}/contents/movies/wishes?order=runtime_short'
    driver.get(url)
    time.sleep(2)

    # 페이지 로드
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(1)
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source)
    raw = soup.find_all("li", class_="zK9dEEA5")
    contents = [r.find("a").get("href").split('/')[-1] for r in raw]

    # driver.quit()

    return contents


def update_data(user_key, df, contents):
    """기존 데이터와 비교 후 업데이트"""

    existing_contents = set(df['content_id'].tolist())
    contents_to_add = list(set(contents) - existing_contents)
    contents_to_remove = list(existing_contents - set(contents))

    df = df.loc[~df['content_id'].isin(contents_to_remove)].reset_index(drop=True)

    session = new_session()

    for content_id in contents_to_add:
        url = f'https://pedia.watcha.com/ko-KR/contents/{content_id}'
        response = session.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        try:
            raw = soup.find("div", class_="sEtpm1Zv J0ALB7d7")
            raw1 = raw.find("div")

            title_ko = raw1.find("h1").get_text()
            try:
                [[title_en], [year, _, country], [running_time, age]] = [r.get_text().split(' · ') for r in raw1.find_all("div")[:3]]
            except:
                [[title_en], [year, _, country], [running_time]] = [r.get_text().split(' · ') for r in raw1.find_all("div")[:3]]

            running_mins = running_min(running_time)

            if raw.find("ul") is None:
                ott_img, ott_tag = [], ''
            else:
                ott_img = [r.find("div").get("style").split('("')[1].split('")')[0] for r in raw.find("ul").find_all("a")]
                ott_list = [dict_ott.get(img, "Unknown") for img in ott_img]
                ott_tag = '#' + '#'.join(ott_list)

            avg_score = soup.find("div", class_="tG5M99eW PZqhmqar").get_text() if soup.find("div", class_="tG5M99eW PZqhmqar") else ''
            img = soup.find("img").get("src")

            df.loc[len(df)] = [content_id, title_ko, title_en, running_mins, running_time, year, country, age, ott_img, ott_tag, avg_score, img]

        except:
            continue

    return df


def runningtime_categories(df, user_key):
    """러닝타임에 따른 카테고리"""

    df_final = df.copy()

    bins1 = [0] + list(range(60, 240, 30)) + [900]; labels1 = [0] + list(range(60, 240, 30))  # 이상
    df_final['time_type1'] = pd.cut(df_final['running_min'], bins=bins1, labels=labels1).astype(float)

    bins2 = [0, 30] + list(range(60, 240, 10)) + [900]; labels2 = [30] + list(range(60, 250, 10))  # 이하
    df_final['time_type2'] = pd.cut(df_final['running_min'], bins=bins2, labels=labels2).astype(float)

    dict_cat = dict(zip(labels1, ['1시간 이하', '1시간 ~ 1시간 30분', '1시간 30분 ~ 2시간', 
                                  '2시간 ~ 2시간 30분', '2시간 30분 ~ 3시간', '3시간 ~ 3시간 30분', '3시간 30분 이상']))
    df_final['category_1d'] = df_final['time_type1'].map(dict_cat)
    df_final['category_2d'] = df_final['time_type2'] - df_final['time_type1']

    return df_final
