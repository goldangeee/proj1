import streamlit as st
from streamlit_folium import st_folium
import folium
import json
import pandas as pd
# import matplotlib.pyplot as plt

# 상단에 타이틀과 설명을 배치
st.title("My ideal region")
st.write("왼쪽 사이드바에서 원하는 버튼을 클릭")
st.write("순위를 확인하려면")
st.write("왼쪽 사이드바에서 순위 확인 버튼을 누른 뒤")
st.write("지역을 클릭해서 팝업을 확인해주세요.")

# 대한민국 지도 경계 데이터
with open("SIDO_MAP_2022_cp949.json", "r", encoding='cp949') as f:
    geo_data = json.load(f)

##################################################################
    
# 인구 밀도 데이터
pop_den = pd.read_csv("pop_den.csv", encoding='utf-8') # 명/㎢
pop_den_df = pd.DataFrame(pop_den)
filtered_pop_den_df = pop_den_df[['행정구역별', '2022']]

# "전국" 행을 제외
new_pop_den_df = filtered_pop_den_df.drop(filtered_pop_den_df[filtered_pop_den_df['행정구역별'] == '전국'].index)
new_pop_den_df['rank'] = new_pop_den_df['2022'].rank(method='min').astype(int) # 데이터프레임에 "rank" 열 생성과 순위 추가

###################################################################################################################

# 초미세먼지(PM2.5) 데이터를 불러옵니다.
pm25 = pd.read_csv("PM25.csv", encoding='utf-8')# ㎍/m³
pm25_df = pd.DataFrame(pm25)

# '구분(1)'과 '구분(2)'의 값이 같거나, '구분(2)'의 값이 '도평균'인 행만 필터링합니다.
filtered_pm25_df = pm25_df[(pm25_df['구분(1)'] == pm25_df['구분(2)']) | (pm25_df['구분(2)'] == '도평균')]

# 필요한 컬럼만 선택합니다. 여기서는 '구분(1)', '구분(2)', '2023.07' 컬럼을 선택합니다.
res_pm25_df = filtered_pm25_df[['구분(1)', '구분(2)', '2023.07']]

new_pm25_df = res_pm25_df[['구분(1)', '2023.07']]
new_pm25_df['rank'] = new_pm25_df['2023.07'].rank(method='min').astype(int) 
# 데이터프레임에 "rank" 열 생성과 순위 추가

# 에러 해결을 위해 안전한 숫자로 변환
res_pm25_df['2023.07'] = pd.to_numeric(res_pm25_df['2023.07'], errors='coerce')

###################################################################################################################

# 교통사고 사망자 수 데이터를 불러옵니다.
car_acc = pd.read_csv("car_acc.csv", encoding='utf-8')# 인구10만명당 사망자수 (명)
car_acc_df = pd.DataFrame(car_acc)

filtered_car_acc_df_1 = car_acc_df[(car_acc_df['행정구역별(1)'] != '총계')&(car_acc_df['행정구역별(2)'] == '소계')]
filtered_car_acc_df_2 = filtered_car_acc_df_1[['행정구역별(1)',filtered_car_acc_df_1.columns[6]]]
filtered_car_acc_df_2.iloc[:, 1] = pd.to_numeric(filtered_car_acc_df_2.iloc[:, 1], errors='coerce') # 에러 해결을 위해 안전한 숫자로 변환
filtered_car_acc_df_2['rank'] = filtered_car_acc_df_2['2020.4'].rank(method='min').astype(int) # 데이터프레임에 "rank" 열 생성과 순위 추가

# 강원특별자치도를 강원도로 통일
filtered_car_acc_df_2['행정구역별(1)'].replace("강원특별자치도", "강원도", inplace=True)

###################################################################################

# 사이드바

# 세션 상태에 'init_state' 속성이 없으면 False로 초기화
if "init_state" not in st.session_state:
    st.session_state.init_state = False

# 세션 상태에 'show_density' 속성이 없으면 False로 초기화
if "show_density" not in st.session_state:
    st.session_state.show_density = False

# 세션 상태에 'show_pm' 속성이 없으면 False로 초기화
if "show_pm" not in st.session_state:
    st.session_state.show_pm = False

# 세션 상태에 'show_caracc' 속성이 없으면 False로 초기화
if "show_caracc" not in st.session_state:
    st.session_state.show_caracc = False
    
# 사이드바에 지도 초기화 버튼을 추가
show_init_state = st.sidebar.button("순위 확인")
if show_init_state:
    st.session_state.show_init_state = True
    st.session_state.show_density = False
    st.session_state.show_pm = False
    st.session_state.show_caracc = False 

# 사이드바에 인구 밀도 버튼을 추가
show_density = st.sidebar.button("지역별 인구밀도")
if show_density:
    st.session_state.show_init_state = False
    st.session_state.show_density = True
    st.session_state.show_pm = False
    st.session_state.show_caracc = False 

# 사이드바에 미세먼지 버튼을 추가
show_pm = st.sidebar.button("지역별 초미세먼지 농도")
if show_pm:
    st.session_state.show_init_state = False
    st.session_state.show_density = False
    st.session_state.show_pm = True    
    st.session_state.show_caracc = False 

# 사이드바에 교통사고 사망자 수 버튼을 추가
show_caracc = st.sidebar.button("교통사고 사망자 수")
if show_caracc:
    st.session_state.show_init_state = False
    st.session_state.show_density = False
    st.session_state.show_pm = False   
    st.session_state.show_caracc = True 

#########################################################

# 지도 객체를 생성합니다.
m = folium.Map(location=[36, 128], zoom_start=6.5)

############################################################

for feature in geo_data['features']:
    ctp_kor_nm = feature['properties']['CTP_KOR_NM']
    data1 = new_pop_den_df.loc[new_pop_den_df["행정구역별"] == ctp_kor_nm, 'rank'].values
    data2 = new_pm25_df.loc[new_pm25_df["구분(1)"] == ctp_kor_nm, 'rank'].values
    data3 = filtered_car_acc_df_2.loc[filtered_car_acc_df_2.iloc[:, 0] == ctp_kor_nm, 'rank'].values   
    feature['properties']['인구밀도 순위'] = str(data1[0]) if len(data1) > 0 else ''
    feature['properties']['공기질 순위'] = str(data2[0]) if len(data2) > 0 else ''
    feature['properties']['교통사고 순위'] = str(data3[0]) if len(data3) > 0 else ''

##############################################################################################

# GeoJSON 레이어를 지도에 추가
folium.GeoJson(
    geo_data,
    name = 'geojson',
    style_function = lambda x: {'fillColor': '#ffffff00'},
    highlight_function = lambda x: {'weight':3, 'color':'blue'},    
    popup=folium.GeoJsonPopup(fields=['인구밀도 순위', '공기질 순위','교통사고 순위'],        
        labels=True,
        localize=True,        
        parse_html=True)                 
).add_to(m)

##################################################################################

# 버튼을 누르면, Choropleth 맵을 생성
if st.session_state.show_density:
    folium.Choropleth(
        geo_data=geo_data,
        name='choropleth1',
        data=pop_den_df,
        columns=['행정구역별', '2022'],  
        key_on='feature.properties.CTP_KOR_NM',  
        fill_color='YlOrRd',  # 색상 팔레트
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='(단위: 명/㎢)'
    ).add_to(m)
elif st.session_state.show_pm:
    folium.Choropleth(
        geo_data=geo_data,
        name='choropleth2',
        data=res_pm25_df,
        columns=['구분(1)', '2023.07'],  
        key_on='feature.properties.CTP_KOR_NM',
        fill_color='YlOrRd',  
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='(단위: μg/m³)'
    ).add_to(m)
elif st.session_state.show_caracc:
    folium.Choropleth(
        geo_data=geo_data,
        name='choropleth3',
        data=filtered_car_acc_df_2,
        columns=['행정구역별(1)', '2020.4'],  
        key_on='feature.properties.CTP_KOR_NM',
        fill_color='YlOrRd',  
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='(인구10만명당 사망자수 (명))'
    ).add_to(m)

# 지도를 표시
st_folium(m, width=700, height=600)

# 지표를 체크박스로 선택하는 기능
# 점수 합산 데이터 프레임 만들기
# 선택한 지표들로 점수를 합산하는 기능