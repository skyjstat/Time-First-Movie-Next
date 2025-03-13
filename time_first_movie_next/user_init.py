"""

서비스 최초 1회 등록
왓챠피디아 로그인 & 유저 키 수집

"""


import json
import os
import time
import warnings
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.utils import is_error 
warnings.filterwarnings('ignore')


def login(driver, user_email, user_pw):
    """왓챠피디아 로그인"""

    url = 'https://pedia.watcha.com/ko-KR/'
    driver.get(url)
    time.sleep(1.5)

    # 팝업 닫기
    if not is_error(driver.find_element, By.XPATH, "//button[text()='닫기']"):
        driver.find_element(By.XPATH, "//button[text()='닫기']").click()

    # 로그인 버튼 클릭
    driver.find_element(By.XPATH, '//button[@data-select="header-sign-in"]').click()
    time.sleep(0.5)

    # 아이디 & 비밀번호 입력
    elements = driver.find_elements(By.XPATH, '//label[@class="gG3A_Mwd"]')
    elements[0].send_keys(user_email)
    elements[1].send_keys(user_pw)

    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(2)


def get_user_key(driver):
    """유저 키 수집"""

    time.sleep(2)
    
    # 팝업 닫기
    if not is_error(driver.find_element, By.XPATH, "//button[text()='닫기']"):
        driver.find_element(By.XPATH, "//button[text()='닫기']").click()
        time.sleep(0.5)

    # 마이페이지 이동
    driver.find_element(By.CSS_SELECTOR, "li[class$='myPage']").click()
    time.sleep(0.5)

    # 유저 키 추출
    return driver.current_url.split('/')[-1]


def save_user_info(user_email, user_key):
    """유저 정보 (ID, 키) 저장"""

    with open("data/user/user_info.json", "r") as f:
        user_info = json.load(f)

    user_info[user_email] = user_key
    pd.DataFrame(columns=['content_id', 'title_ko', 'title_en', 'running_min', 'running_time', 'year', 'country', 'age', 'ott_img', 'ott_tag', 'avg_score', 'img'])\
        .to_csv(f"data/raw/data_{user_key}.csv")

    with open("data/user/user_info.json", "w") as f:
        json.dump(user_info, f)


# def main():
#     user_email = input('왓챠피디아 ID : ')
#     user_pw = input('왓챠피디아 PW : ')

#     driver = webdriver.Chrome()

#     try:
#         # 로그인 & 유저 키 수집
#         login(driver, user_email, user_pw)
#         user_key = get_user_key(driver)

#         # 유저 정보 저장
#         save_user_info(user_email, user_key)

#     except Exception as e:
#         print(f"🚨 오류 발생: {e}")

#     finally:
#         driver.quit()


# if __name__ == "__main__":
#     main()