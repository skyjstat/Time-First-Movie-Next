import streamlit as st
from streamlit_image_select import image_select
import pandas as pd
from utils_streamlit import process_image, is_error, category, load_fonts
from streamlit_javascript import st_javascript
import math


def floor_to_tens(x):
    return math.floor(x / 10) * 10

col_width = floor_to_tens(st_javascript("window.innerWidth")/4)


def main_contents(rows, tmp):
    for r in range(rows):
        now = tmp.loc[(4*r):(4*r+3)]

        image = [process_image(url, col_width) for url in now['img']]
        title = now['title_ko'].tolist(); running_time = now['running_time'].tolist()
        year = now['year'].tolist(); country = now['country'].tolist(); age = now['age'].tolist(); ott_tag = now['ott_tag'].tolist()
        url = ['https://pedia.watcha.com/ko-KR/contents/' + content_id for content_id in now['content_id']]
        
        cols = st.columns(4)
        for i, c in enumerate(cols):
            with c:
                try:
                    st.image(image[i])
                    st.markdown(f"""
                                <div>
                                    <a href="{url[i]}" target="_blank" style="text-decoration: none; color: inherit;">
                                        <p class="pretendard-bold" style="font-size:16px; margin-bottom:3px; margin-top:0px; cursor: pointer;">
                                            {title[i]} ({year[i]})
                                        </p>
                                    </a>
                                    <p class="pretendard-semibold" style="font-size:14px; margin-bottom:5px;">{running_time[i]}</p>
                                    <p class="pretendard-medium" style="font-size:12px; color:gray; margin-bottom:6px;">{age[i]} · {country[i]}</p>
                                </div>
                                """, unsafe_allow_html=True)
                    st.markdown('<div style="margin-bottom: 16px;">' + " ".join([f'<span class="static-button">{tag}</span>' for tag in ott_tag[i]]) + "</div>", unsafe_allow_html=True)
                except:
                    st.write("")


def data_preprocess(df):
    df = df.sort_values(by='running_min').reset_index(drop=True)
    df['category_2d'] = df['category_2d'].astype(int)
    df['ott_tag'] = df['ott_tag'].str.split('#').str[1:]

    return df


def main(df, options_ott):
    load_fonts()


    if not options_ott:
        df = df.copy()
    else:
        df = df.loc[df["ott_tag"].apply(lambda x: isinstance(x, list) and any(tag in x for tag in options_ott))].reset_index(drop=True).copy()


    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(category)

    with tab1:
        cat_tab1 = category[0]
        st.markdown(f"""<p class="pretendard-bold" style="font-size:24px; margin-bottom:6px; margin-top:10px">{cat_tab1}</p>""", unsafe_allow_html=True)

        df1 = df.loc[df['category_1d'] == cat_tab1]
        if len(df1) == 0:
            st.markdown(f"""<p class="pretendard-medium" style="font-size:18px; color:gray; margin-top:14px">러닝타임이 {cat_tab1}인 영화가 '보고싶어요'에 없어요.</p>""", unsafe_allow_html=True)
        else:
            sub_tab1 = df1.category_2d.unique().tolist()
        
            for sub in sorted(sub_tab1):
                if sub == 30:
                    st.markdown('<p class="pretendard-medium" style="font-size:20px; margin-top:14px">~ 30분</p>', unsafe_allow_html=True)
                else:
                    st.markdown('<p class="pretendard-medium" style="font-size:20px; margin-top:14px">~ 1시간 </p>', unsafe_allow_html=True)
                tmp = df1.loc[df1['category_2d'] == sub].reset_index(drop=True)
                rows = len(tmp)//4 + 1

                main_contents(rows, tmp)


    with tab2:
        cat_tab2 = category[1]
        st.markdown(f"""<p class="pretendard-bold" style="font-size:24px; margin-bottom:6px; margin-top:10px">{cat_tab2}</p>""", unsafe_allow_html=True)

        df2 = df.loc[df['category_1d'] == cat_tab2]
        if len(df2) == 0:
            st.markdown(f"""<p class="pretendard-medium" style="font-size:18px; color:gray; margin-top:14px">러닝타임이 {cat_tab2}인 영화가 '보고싶어요'에 없어요.</p>""", unsafe_allow_html=True)
        else:
            sub_tab2 = df2.category_2d.unique().tolist()
        
            for sub in sorted(sub_tab2):
                st.markdown(f'<p class="pretendard-medium" style="font-size:20px; margin-top:14px">~ 1시간 {sub}분</p>', unsafe_allow_html=True)
                tmp = df2.loc[df2['category_2d'] == sub].reset_index(drop=True)
                rows = len(tmp)//4 + 1

                main_contents(rows, tmp)


    with tab3:
        cat_tab3 = category[2]
        st.markdown(f"""<p class="pretendard-bold" style="font-size:24px; margin-bottom:6px; margin-top:10px">{cat_tab3}</p>""", unsafe_allow_html=True)

        df3 = df.loc[df['category_1d'] == cat_tab3]
        if len(df3) == 0:
            st.markdown(f"""<p class="pretendard-medium" style="font-size:18px; color:gray; margin-top:14px">러닝타임이 {cat_tab3}인 영화가 '보고싶어요'에 없어요.</p>""", unsafe_allow_html=True)
        else:
            sub_tab3 = df3.category_2d.unique().tolist()
        
            for sub in sorted(sub_tab3):
                if sub != 30:
                    st.markdown(f'<p class="pretendard-medium" style="font-size:20px; margin-top:14px">~ 1시간 {30 + sub}분</p>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<p class="pretendard-medium" style="font-size:20px;">~ 2시간 </p>', unsafe_allow_html=True)
                tmp = df3.loc[df3['category_2d'] == sub].reset_index(drop=True)
                rows = len(tmp)//4 + 1

                main_contents(rows, tmp)


    with tab4:
        cat_tab4 = category[3]
        st.markdown(f"""<p class="pretendard-bold" style="font-size:24px; margin-bottom:6px; margin-top:10px">{cat_tab4}</p>""", unsafe_allow_html=True)

        df4 = df.loc[df['category_1d'] == cat_tab4]
        if len(df4) == 0:
            st.markdown(f"""<p class="pretendard-medium" style="font-size:18px; color:gray; margin-top:14px">러닝타임이 {cat_tab4}인 영화가 '보고싶어요'에 없어요.</p>""", unsafe_allow_html=True)
        else:
            sub_tab4 = df4.category_2d.unique().tolist()
        
            for sub in sorted(sub_tab4):
                st.markdown(f'<p class="pretendard-medium" style="font-size:20px; margin-top:14px">~ 2시간 {sub}분</p>', unsafe_allow_html=True)
                tmp = df4.loc[df4['category_2d'] == sub].reset_index(drop=True)
                rows = len(tmp)//4 + 1

                main_contents(rows, tmp)


    with tab5:
        cat_tab5 = category[4]
        st.markdown(f"""<p class="pretendard-bold" style="font-size:24px; margin-bottom:6px; margin-top:10px">{cat_tab5}</p>""", unsafe_allow_html=True)

        df5 = df.loc[df['category_1d'] == cat_tab5]
        if len(df5) == 0:
            st.markdown(f"""<p class="pretendard-medium" style="font-size:18px; color:gray; margin-top:14px">러닝타임이 {cat_tab5}인 영화가 '보고싶어요'에 없어요.</p>""", unsafe_allow_html=True)
        else:
            sub_tab5 = df5.category_2d.unique().tolist()
        
            for sub in sorted(sub_tab5):
                if sub != 30:
                    st.markdown(f'<p class="pretendard-medium" style="font-size:20px; margin-top:14px">~ 2시간 {30 + sub}분</p>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<p class="pretendard-medium" style="font-size:20px;">~ 3시간 </p>', unsafe_allow_html=True)
                tmp = df5.loc[df5['category_2d'] == sub].reset_index(drop=True)
                rows = len(tmp)//4 + 1

                main_contents(rows, tmp)


    with tab6:
        cat_tab6 = category[5]
        st.markdown(f"""<p class="pretendard-bold" style="font-size:24px; margin-bottom:6px; margin-top:10px">{cat_tab6}</p>""", unsafe_allow_html=True)

        df6 = df.loc[df['category_1d'] == cat_tab6]
        if len(df6) == 0:
            st.markdown(f"""<p class="pretendard-medium" style="font-size:18px; color:gray; margin-top:14px">러닝타임이 {cat_tab6}인 영화가 '보고싶어요'에 없어요.</p>""", unsafe_allow_html=True)
        else:
            sub_tab6 = df6.category_2d.unique().tolist()
        
            for sub in sorted(sub_tab6):
                st.markdown(f'<p class="pretendard-medium" style="font-size:20px; margin-top:14px">~ 3시간 {sub}분</p>', unsafe_allow_html=True)
                tmp = df6.loc[df6['category_2d'] == sub].reset_index(drop=True)
                rows = len(tmp)//4 + 1

                main_contents(rows, tmp)


    with tab7:
        cat_tab7 = category[6]
        st.markdown(f"""<p class="pretendard-bold" style="font-size:24px; margin-bottom:6px; margin-top:10px">{cat_tab7}</p>""", unsafe_allow_html=True)

        df7 = df.loc[df['category_1d'] == cat_tab7]
        if len(df7) == 0:
            st.markdown(f"""<p class="pretendard-medium" style="font-size:18px; color:gray; margin-top:14px">러닝타임이 {cat_tab7}인 영화가 '보고싶어요'에 없어요.</p>""", unsafe_allow_html=True)
        else:
            sub_tab7 = df7.category_2d.unique().tolist()
        
            for sub in sorted(sub_tab7):
                tmp = df7.loc[df7['category_2d'] == sub].reset_index(drop=True)
                rows = len(tmp)//4 + 1

                main_contents(rows, tmp)

                