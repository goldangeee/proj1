import streamlit as st
from streamlit_folium import st_folium
import folium
import json
import pandas as pd

# 상단에 타이틀과 설명을 배치
st.title("My ideal region")
# 사이드바
# 세션 상태에 특정 속성이 없으면 False로 초기화
if "init_state" not in st.session_state:
    st.session_state.init_state = False
if "show_density" not in st.session_state:
    st.session_state.show_density = False
if "show_pm" not in st.session_state:
    st.session_state.show_pm = False
if "show_caracc" not in st.session_state:
    st.session_state.show_caracc = False   
if "show_recommend" not in st.session_state:
    st.session_state.show_recommend = False   
# 홈 버튼
show_init_state = st.sidebar.button("홈")
if show_init_state:
    st.session_state.show_init_state = True
    st.session_state.show_density = False
    st.session_state.show_pm = False
    st.session_state.show_caracc = False
    st.session_state.show_recommend = False  
# 인구 밀도 버튼 및 체크박스
show_density = st.sidebar.button("[인구] 인구 밀도")  # 버튼
if "density_checked" not in st.session_state:  # 세션 상태에 체크박스 상태를 저장할 키가 없으면 초기화
    st.session_state.density_checked = False
density_checked = st.sidebar.checkbox("인구 밀도", key="density_checked")  # 체크박스
if show_density:  # 버튼 눌림 또는 체크박스 체크 상태일 때
    st.session_state.show_init_state = False
    st.session_state.show_density = True
    st.session_state.show_pm = False
    st.session_state.show_caracc = False
    st.session_state.show_recommend = False 
# 초미세먼지 버튼 및 체크박스
show_pm = st.sidebar.button("[환경] 초미세먼지 농도")  # 버튼
if "pm_checked" not in st.session_state:
    st.session_state.pm_checked = False
pm_checked = st.sidebar.checkbox("초미세먼지 농도", key="pm_checked")  # 체크박스
if show_pm:
    st.session_state.show_init_state = False
    st.session_state.show_density = False
    st.session_state.show_pm = True    
    st.session_state.show_caracc = False
    st.session_state.show_recommend = False  
# 교통사고 사망자 수 버튼 및 체크박스
show_caracc = st.sidebar.button("[안전] 교통사고 사망자 수")  # 버튼
if "caracc_checked" not in st.session_state:
    st.session_state.caracc_checked = False
caracc_checked = st.sidebar.checkbox("교통사고 사망자 수", key="caracc_checked")  # 체크박스
if show_caracc:
    st.session_state.show_init_state = False
    st.session_state.show_density = False
    st.session_state.show_pm = False   
    st.session_state.show_caracc = True
    st.session_state.show_recommend = False 
# 지역 추천
show_recommend = st.sidebar.button("지역 추천")
if show_recommend:
    st.session_state.show_init_state = False
    st.session_state.show_density = False
    st.session_state.show_pm = False
    st.session_state.show_caracc = False
    st.session_state.show_recommend = True      

# 화면 분할
col1, col2 = st.columns([5, 4])

# 데이터
# 대한민국 지도 경계 데이터
with open("SIDO_MAP_2022_cp949.json", "r", encoding='cp949') as f:
    geo_data = json.load(f)    
# 인구 밀도 데이터
pop_den = pd.read_csv("pop_den.csv", encoding='utf-8') # 명/㎢
pop_den_df = pd.DataFrame(pop_den)
filtered_pop_den_df = pop_den_df[['행정구역별', '2022']]
new_pop_den_df = filtered_pop_den_df.drop(filtered_pop_den_df[filtered_pop_den_df['행정구역별'] == '전국'].index) # "전국" 행을 제외
new_pop_den_df['순위'] = new_pop_den_df['2022'].rank(method='min').astype(int) # 데이터프레임에 "순위" 열 생성과 순위 추가
new_pop_den_df = new_pop_den_df.rename(columns={'행정구역별': '지역', '2022': '인구 밀도'})
new_pop_den_df = new_pop_den_df.sort_values(by='인구 밀도')
# 초미세먼지(PM2.5) 데이터
pm25 = pd.read_csv("PM25.csv", encoding='utf-8')
pm25_df = pd.DataFrame(pm25)
filtered_pm25_df = pm25_df[(pm25_df['구분(1)'] == pm25_df['구분(2)']) | (pm25_df['구분(2)'] == '도평균')] # '구분(1)'과 '구분(2)'의 값이 같거나, '구분(2)'의 값이 '도평균'인 행만 필터링
filtered_pm25_df = filtered_pm25_df[['구분(1)','2023.07']] # 필요한 컬럼만 선택
filtered_pm25_df['순위'] = filtered_pm25_df['2023.07'].rank(method='min').astype(int) # 데이터프레임에 "순위" 열 생성과 순위 추가
filtered_pm25_df['2023.07'] = pd.to_numeric(filtered_pm25_df['2023.07'], errors='coerce') # 에러 해결을 위해 안전한 숫자로 변환
filtered_pm25_df = filtered_pm25_df.rename(columns={'구분(1)': '지역', '2023.07': 'PM2.5 농도'})
filtered_pm25_df = filtered_pm25_df.sort_values(by='PM2.5 농도')
# 교통사고 사망자 수 데이터
car_acc = pd.read_csv("car_acc.csv", encoding='utf-8')# 인구10만명당 사망자수 (명)
car_acc_df = pd.DataFrame(car_acc)
filtered_car_acc_df_1 = car_acc_df[(car_acc_df['행정구역별(1)'] != '총계')&(car_acc_df['행정구역별(2)'] == '소계')]
filtered_car_acc_df_2 = filtered_car_acc_df_1[['행정구역별(1)',filtered_car_acc_df_1.columns[6]]]
filtered_car_acc_df_2.iloc[:, 1] = pd.to_numeric(filtered_car_acc_df_2.iloc[:, 1], errors='coerce') # 에러 해결을 위해 안전한 숫자로 변환
filtered_car_acc_df_2['순위'] = filtered_car_acc_df_2['2020.4'].rank(method='min').astype(int) # 데이터프레임에 "순위" 열 생성과 순위 추가
filtered_car_acc_df_2['행정구역별(1)'].replace("강원특별자치도", "강원도", inplace=True) # 강원특별자치도를 강원도로 변경
filtered_car_acc_df_2 = filtered_car_acc_df_2.rename(columns={'행정구역별(1)': '지역', '2020.4': '교통사고'})
filtered_car_acc_df_2 = filtered_car_acc_df_2.sort_values(by='교통사고')

# 지도 객체를 생성합니다.
m = folium.Map(location=[36, 131], zoom_start=6.4)

for feature in geo_data['features']:
    ctp_kor_nm = feature['properties']['CTP_KOR_NM']
    data1 = new_pop_den_df.loc[new_pop_den_df["지역"] == ctp_kor_nm, '순위'].values
    data2 = filtered_pm25_df.loc[filtered_pm25_df["지역"] == ctp_kor_nm, '순위'].values
    data3 = filtered_car_acc_df_2.loc[filtered_car_acc_df_2.iloc[:, 0] == ctp_kor_nm, '순위'].values   
    feature['properties']['인구밀도 순위 : '] = str(data1[0]) if len(data1) > 0 else ''
    feature['properties']['공기질 순위 : '] = str(data2[0]) if len(data2) > 0 else ''
    feature['properties']['교통안전 순위 : '] = str(data3[0]) if len(data3) > 0 else ''

##############################################################################################

# GeoJSON 레이어를 지도에 추가
folium.GeoJson(
    geo_data,
    name = 'geojson',
    style_function = lambda x: {'fillColor': '#ffffff00'},
    highlight_function = lambda x: {'weight':3, 'color':'blue'},    
    popup=folium.GeoJsonPopup(fields=['인구밀도 순위 : ', '공기질 순위 : ','교통안전 순위 : '],        
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
        data=new_pop_den_df,
        columns=['지역', '인구 밀도'],  
        key_on='feature.properties.CTP_KOR_NM',  
        fill_color='YlOrRd',  # 색상 팔레트
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='(단위: 명/㎢)'
    ).add_to(m)
    with col2:
        st.write(new_pop_den_df)
elif st.session_state.show_pm:
    folium.Choropleth(
        geo_data=geo_data,
        name='choropleth2',
        data=filtered_pm25_df,
        columns=['지역', 'PM2.5 농도'],  
        key_on='feature.properties.CTP_KOR_NM',
        fill_color='YlOrRd',  
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='(단위: μg/m³)'
    ).add_to(m)
    with col2:
        st.write(filtered_pm25_df)
elif st.session_state.show_caracc:
    folium.Choropleth(
        geo_data=geo_data,
        name='choropleth3',
        data=filtered_car_acc_df_2,
        columns=['지역', '교통사고'],  
        key_on='feature.properties.CTP_KOR_NM',
        fill_color='YlOrRd',  
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='(인구10만명당 사망자수 (명))'
    ).add_to(m)
    with col2:
        st.write(filtered_car_acc_df_2)

# 지도를 표시
with col1:
    st_folium(m, width=700, height=600)

recommended_region_df = new_pop_den_df[["지역"]]
recommended_region_df['포인트'] = 0
df2 = recommended_region_df

if density_checked:
    df1 = new_pop_den_df
    # "지역"을 기준으로 두 데이터 프레임을 병합
    merged_df = pd.merge(df1, df2, on="지역")    
    # # 병합된 데이터 프레임에서 순위를 더함
    merged_df['포인트'] = merged_df['순위'] + merged_df['포인트']
    df2 = merged_df[['지역', '포인트']]

if pm_checked:
    df1 = filtered_pm25_df
    # "지역"을 기준으로 두 데이터 프레임을 병합
    merged_df = pd.merge(df1, df2, on="지역")    
    # # 병합된 데이터 프레임에서 순위를 더함
    merged_df['포인트'] = merged_df['순위'] + merged_df['포인트']
    df2 = merged_df[['지역', '포인트']]

if caracc_checked:
    df1 = filtered_car_acc_df_2
    # "지역"을 기준으로 두 데이터 프레임을 병합
    merged_df = pd.merge(df1, df2, on="지역")    
    # # 병합된 데이터 프레임에서 순위를 더함
    merged_df['포인트'] = merged_df['순위'] + merged_df['포인트']
    df2 = merged_df[['지역', '포인트']]

if st.session_state.show_recommend:
    with col2:
        st.write(f"포인트가 낮을수록 추천하는 지역입니다.")
        st.write(df2.sort_values(by='포인트'))
        