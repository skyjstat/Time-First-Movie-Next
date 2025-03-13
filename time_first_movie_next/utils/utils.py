from selenium import webdriver
import time
import requests

dict_ott = {"왓챠": "https://an2-glx.amz.wtchn.net/images/ex_watcha_logo_square.png",
            "넷플릭스": "https://an2-glx.amz.wtchn.net/images/ex_netflix_logo_square.png",
            "티빙": "https://an2-img.amz.wtchn.net/image/v2/AmxtezC90nGQwOmwj0MCPA.png?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKd0lqb2lMM1l5TDNOMGIzSmxMM1ZwYldGblpTOHhOalV3TXpRMk9UQXhNVE0xTlRBNU16TTRJbjAudWd0X0VwOHg1ZDBnZTBTRjhiNkhrUG52Qzd5cndhRnl6bEt2dEZzVGhzTQ",
            "디즈니+": "https://an2-img.amz.wtchn.net/image/v2/mPQV0ogd6uw4_5DmR0oBFA.png?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKd0lqb2lMM1l5TDNOMGIzSmxMM1ZwYldGblpTODJPVE14TmpNeE1qWXpNekE1TURraWZRLnZ0TFJSVWFtRWtJRDBHMFJnZGdQVC1WWlJLckE3eGNHZWdpMFpWWXhWZWM&ts=1712645394",
            "웨이브": "https://an2-glx.amz.wtchn.net/images/ex_wavve_logo_square.png",
            "애플TV": "https://an2-img.amz.wtchn.net/image/v2/b3bcd21bde7b191df6fa694ccd311e47.png?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKd1lYUm9Jam9pTDNZeUwzTjBiM0psTDNWcGJXRm5aUzh4TmpNM01qSTFNREl3TWpVNE16RTBNVFV5SW4wLjVxOGpmdThiY0NWOXg1QVFTVDlRSnlVTHFwWDNZMmxpWWpMSXFqdkwzMUE"}
dict_ott = dict(zip(dict_ott.values(), dict_ott.keys()))

def is_error(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
        return False 
    except Exception:
        return True 


def running_min(running_time):
    if '시간' in running_time:
        if '분' in running_time:
            tmp = running_time.split(' ')
            h = int(tmp[0].split('시간')[0])
            m = int(tmp[1].split('분')[0])
        else:
            h = int(running_time.split('시간')[0]); m = 0
    else:
        m = int(running_time.split('분')[0]); h = 0
    
    res = 60*h + m
    
    return res


def new_session():
    # WebDriver 생성
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--disable-notifications")
    chromeOptions.add_argument("--headless")

    # 왓챠피디아 이동, 쿠키 추출 
    driver = webdriver.Chrome(options=chromeOptions)
    driver.get("https://pedia.watcha.com/ko-KR/")
    time.sleep(1)

    cookies = driver.get_cookies()
    cookies_new = {cookie['name']: cookie['value'] for cookie in cookies}

    driver.quit()

    # 세션 생성, 쿠키 입력 
    session = requests.Session()
    session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    session.cookies.update(cookies_new)
    
    return session