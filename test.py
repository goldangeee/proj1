import streamlit as st
from streamlit_folium import st_folium
import folium
import json
import pandas as pd

# 상단에 타이틀과 설명을 배치합니다.
st.title("My ideal region")
st.write("지역을 클릭해서 지표를 확인해주세요")

# 대한민국 지도 경계 데이터를 불러옵니다.
with open("SIDO_MAP_2022_cp949.json", "r", encoding='cp949') as f:
    geo_data = json.load(f)

##################################################################
    
# 인구 밀도 데이터를 불러옵니다.
pop_den = pd.read_csv("pop_den.csv", encoding='utf-8') # 명/㎢

###################################################################################################################

# 미세먼지(PM2.5) 데이터를 불러옵니다.
pm_25 = pd.read_csv("PM25.csv", encoding='utf-8')# ㎍/m³
pm_df = pd.DataFrame(pm_25)

# '구분(1)'과 '구분(2)'의 값이 같거나, '구분(2)'의 값이 '도평균'인 행만 필터링합니다.
filtered_pm_df = pm_df[(pm_df['구분(1)'] == pm_df['구분(2)']) | (pm_df['구분(2)'] == '도평균')]

# 필요한 컬럼만 선택합니다. 여기서는 '구분(1)', '구분(2)', '2023.07' 컬럼을 선택합니다.
res_pm_df = filtered_pm_df[['구분(1)', '구분(2)', '2023.07']]

###################################################################################

# 세션 상태에 'show_density' 속성이 없으면 False로 초기화합니다.
if "show_density" not in st.session_state:
    st.session_state.show_density = False

# 세션 상태에 'show_pm' 속성이 없으면 False로 초기화합니다.
if "show_pm" not in st.session_state:
    st.session_state.show_pm = False
    
# 사이드바에 인구 밀도 버튼을 추가합니다.
show_density = st.sidebar.button("인구 밀도 보기")
if show_density:
    st.session_state.show_density = True
    st.session_state.show_pm = False

# 사이드바에 미세먼지 버튼을 추가합니다.
show_pm = st.sidebar.button("미세먼지 농도 보기")
if show_pm:
    st.session_state.show_pm = True
    st.session_state.show_density = False

# 지도 객체를 생성합니다.
m = folium.Map(location=[36, 128], zoom_start=6)

# 인구 밀도 버튼을 누르면, Choropleth 맵을 생성합니다.
if st.session_state.show_density:
    folium.Choropleth(
        geo_data=geo_data,
        name='choropleth1',
        data=pop_den,
        columns=['행정구역별', '2022'],  # 여기서 '2022'는 인구 밀도 데이터 컬럼명에 맞게 조정
        key_on='feature.properties.CTP_KOR_NM',  # GeoJSON의 지역 이름 필드에 맞게 조정
        fill_color='YlOrRd',  # 색상 팔레트
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='인구 밀도 단위는 [명/km^2]'
    ).add_to(m)
elif st.session_state.show_pm:
    folium.Choropleth(
        geo_data=geo_data,
        name='choropleth2',
        data=res_pm_df,
        columns=['구분(1)', '2023.07'],  
        key_on='feature.properties.CTP_KOR_NM',
        fill_color='BuGn',  # 색상 팔레트
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='PM2.5 단위는 [마이크로그램/m^3]'
    ).add_to(m)

# 지도를 표시합니다.
st_folium(m, width=1000, height=800)