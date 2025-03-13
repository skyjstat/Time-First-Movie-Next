import streamlit as st
from PIL import Image, ImageOps
import requests
from io import BytesIO
import re


category = ['1시간 이하', '1시간 ~ 1시간 30분', '1시간 30분 ~ 2시간', '2시간 ~ 2시간 30분', '2시간 30분 ~ 3시간', '3시간 ~ 3시간 30분', '3시간 30분 이상']

otts = ["왓챠", "넷플릭스", "티빙", "디즈니+", "웨이브", "애플TV"]


def process_image(url, width):
    response = requests.get(url)
    # width = round(width*0.95); height = round(width*(10/7))  
    img = Image.open(BytesIO(response.content))#.resize((width, height))
    img = ImageOps.expand(img, border=3, fill="white")
    return img


def is_email(user_input):
    EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(EMAIL_REGEX, user_input) is not None


def is_error(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
        return False 
    except Exception:
        return True 


def load_fonts():
    st.markdown(
        """
        <script>
        (function(d) {
            var config = {
            kitId: 'exz4xvk', 
            scriptTimeout: 3000,
            async: true
            },
            h=d.documentElement,t=setTimeout(function(){h.className=h.className.replace(/\bwf-loading\b/g,"")+" wf-inactive";},config.scriptTimeout),tk=d.createElement("script"),f=false,s=d.getElementsByTagName("script")[0],a;h.className+=" wf-loading";tk.src='https://use.typekit.net/'+config.kitId+'.js';tk.async=true;tk.onload=tk.onreadystatechange=function(){a=this.readyState;if(f||a&&a!="complete"&&a!="loaded")return;f=true;clearTimeout(t);try{Typekit.load(config)}catch(e){}};s.parentNode.insertBefore(tk,s)
        })(document);
        </script>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
            body {
                font-family: "pretendard", sans-serif;
            }
            .pretendard-medium {
                font-family: "pretendard", sans-serif;
                font-weight: 500; /* Medium */
            }
            .pretendard-semibold {
                font-family: "pretendard", sans-serif;
                font-weight: 600; /* SemiBold */
            }
            .pretendard-bold {
                font-family: "pretendard", sans-serif;
                font-weight: 700; /* Bold */
            }
            .pretendard-extrabold {
                font-family: "pretendard", sans-serif;
                font-weight: 800; /* ExtraBold */
            }

            .static-button {
                background-color: #f2f2f2; /* 연한 회색 배경 */
                color: gray; /* 검은색 글씨 */
                padding: 3px 8px 2px 8px; /* 내부 여백 */
                font-size: 12px; /* 글꼴 크기 */
                border-radius: 50px; /* 둥근 모서리 */
                display: inline-block; /* 크기 조정 가능 */
                text-align: center;
                width: fit-content; /* 내용 크기에 맞게 조정 */
                font-family: "pretendard", sans-serif; 
                font-weight: 500;
                margin-top: 3px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
