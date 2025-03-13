import streamlit as st
from utils_streamlit import is_email, is_error, category, otts, load_fonts
import pandas as pd
from selenium import webdriver
import sys
import os
import json
import algpy
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import user_init
import access_wishes

def get_path(relative_path):
    BASE_DIR = os.path.abspath(os.path.dirname(__file__)) 
    return os.path.normpath(os.path.join(BASE_DIR, relative_path)) 

load_fonts()

st.image(get_path("img/title.png"))

if "page" not in st.session_state:
    st.session_state["page"] = "home"

def InitialPage():
    st.markdown(
        """
        <div style="text-align: center; margin-top:0px;">
            <p class="pretendard-bold" style="font-size:24px; margin-bottom:0px; color:#595959">Sort by runtime, Watch what fits</p>
            <p class="pretendard-semibold" style="font-size:20px; margin-top:5px; margin-bottom:0px; color:#595959">지금 내게 주어진 시간에 딱 맞는 영화를 찾는 방법</p>
            <p style="margin-bottom:40px"></p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with open(get_path("../data/user/user_info.json"), "r") as f:
        user_info = json.load(f)
    
    col1, col2 = st.columns([1, 1])

    with col1.form(key="login"):
        st.markdown('<p class="pretendard-medium" style="font-size:16px; color:gray; margin-bottom:4px; margin-top:4px;">왓챠피디아 ID를 등록한 적이 있다면</p>'
                    '<p class="pretendard-bold" style="font-size:24px; font-weight:bold; margin-top:0px; margin-bottom:8px;">로그인</p>', unsafe_allow_html=True)
        user_email_login = st.text_input("왓챠피디아 ID", key="login_email")
        logined = st.form_submit_button("로그인")

        if logined:
            if not user_email_login.strip():
                st.warning("왓챠피디아 ID를 입력하세요.")
            elif not is_email(user_email_login):
                st.warning("ID는 이메일 형식입니다.")
            elif user_email_login not in user_info.keys():
                st.warning("등록되지 않은 ID입니다.")
            else:
                st.session_state["user_email_login"] = user_email_login
                st.session_state["page"] = "page_prologue"
                st.rerun()

    with col2.form(key="register"):
        st.markdown('<p class="pretendard-medium" style="font-size:16px; color:gray; margin-bottom:4px; margin-top:4px;">처음이라면</p>'
                    '<p class="pretendard-bold" style="font-size:24px; font-weight:bold; margin-top:0px; margin-bottom:8px; color:#FF0558;">왓챠피디아 ID 등록</p>', unsafe_allow_html=True)
        user_email_register = st.text_input("왓챠피디아 ID", key="register_email")
        user_pw_register = st.text_input("왓챠피디아 PW", type="password", key="register_pw")
        registered = st.form_submit_button("등록")

        if registered:
            if not is_email(user_email_register):
                st.warning("ID는 이메일 형식입니다.")
            elif not user_email_register.strip() or not user_pw_register.strip():
                st.warning("모든 항목을 입력하세요.")
            else:
                st.session_state["user_email_register"] = user_email_register
                st.session_state["user_pw_register"] = user_pw_register
                st.session_state["page"] = "page_register"
                st.rerun()
            

def RegisterPage():
    with open(get_path("../data/user/user_info.json"), "r") as f:
        user_info = json.load(f)
    
    user_email = st.session_state["user_email_register"]
    user_pw = st.session_state["user_pw_register"]
    driver = webdriver.Chrome()

    try:
        with st.spinner("[1/3] 🍿 왓챠피디아 로그인 중..."):
            user_init.login(driver, user_email, user_pw)
        st.success("[1/3] 🍿 왓챠피디아 로그인 성공!")
    except Exception as e:
        st.warning("❕왓챠피디아 로그인 실패: ID/PW를 확인하고, 문제가 없다면 관리자에게 문의하세요.")
        st.write(e)

    try:
        with st.spinner("[2/3] 🔑 유저 키 수집 중..."):
            user_key = user_init.get_user_key(driver)
        st.success("[2/3] 🔑 유저 키 수집 완료! ")
        driver.quit()
    except Exception as e:
        st.warning("❕유저 키 수집 실패: 관리자에게 문의하세요.")
        st.write(e)

    with open(get_path("../data/user/user_info.json"), "r") as f:
        user_info = json.load(f)

    user_info[user_email] = user_key
    pd.DataFrame(columns=['content_id', 'title_ko', 'title_en', 'running_min', 'running_time', 'year', 'country', 'age', 'ott_img', 'ott_tag', 'avg_score', 'img'])\
        .to_csv(get_path(f"../data/raw/df_{user_key}.csv"))

    with open(get_path("../data/user/user_info.json"), "w") as f:
        json.dump(user_info, f)
    st.success("[3/3] 👋🏻 유저 정보 저장 완료!")
