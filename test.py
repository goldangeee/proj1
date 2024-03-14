import streamlit as st
from streamlit_folium import st_folium
import folium
import json
import pandas as pd

# 대한민국 지도 경계 데이터를 불러옵니다.
with open("SIDO_MAP_2022_cp949.json", "r", encoding='cp949') as f:
    geo_data = json.load(f)

# 인구 밀도 데이터를 불러옵니다.
pop_den = pd.read_csv("pop_den.csv", encoding='utf-8')

# 지역별 웹사이트 정보를 추가합니다.
for feature in geo_data['features']:
    if feature['properties']['CTP_KOR_NM'] == '서울특별시':
        feature['properties']['website'] = '서울특별시의 인구밀도(예정)'
    elif feature['properties']['CTP_KOR_NM'] == '부산광역시':
        feature['properties']['website'] = '부산광역시의 인구밀도(예정)'
    elif feature['properties']['CTP_KOR_NM'] == '대구광역시':
        feature['properties']['website'] = '대구광역시의 인구밀도(예정)'
    elif feature['properties']['CTP_KOR_NM'] == '인천광역시':
        feature['properties']['website'] = '인천광역시의 인구밀도(예정)'
    elif feature['properties']['CTP_KOR_NM'] == '광주광역시':
        feature['properties']['website'] = '광주광역시의 인구밀도(예정)'
    elif feature['properties']['CTP_KOR_NM'] == '대전광역시':
        feature['properties']['website'] = '대전광역시의 인구밀도(예정)'
    elif feature['properties']['CTP_KOR_NM'] == '울산광역시':
        feature['properties']['website'] = '울산광역시의 인구밀도(예정)'
    elif feature['properties']['CTP_KOR_NM'] == '세종특별자치시':
        feature['properties']['website'] = '세종특별자치시의 인구밀도(예정)'
    elif feature['properties']['CTP_KOR_NM'] == '경기도':
        feature['properties']['website'] = '경기도의 인구밀도(예정)'
    elif feature['properties']['CTP_KOR_NM'] == '강원도':
        feature['properties']['website'] = '강원도의 인구밀도(예정)'
    elif feature['properties']['CTP_KOR_NM'] == '충청북도':
        feature['properties']['website'] = '충청북도의 인구밀도(예정)'
    elif feature['properties']['CTP_KOR_NM'] == '충청남도':
        feature['properties']['website'] = '충청남도의 인구밀도(예정)'
    elif feature['properties']['CTP_KOR_NM'] == '전라북도':
        feature['properties']['website'] = '전라북도의 인구밀도(예정)'
    elif feature['properties']['CTP_KOR_NM'] == '전라남도':
        feature['properties']['website'] = '전라남도의 인구밀도(예정)'
    elif feature['properties']['CTP_KOR_NM'] == '경상북도':
        feature['properties']['website'] = '경상북도의 인구밀도(예정)'
    elif feature['properties']['CTP_KOR_NM'] == '경상남도':
        feature['properties']['website'] = '경상남도의 인구밀도(예정)'
    elif feature['properties']['CTP_KOR_NM'] == '제주특별자치도':
        feature['properties']['website'] = '제주특별자치도의 인구밀도(예정)'


st.title("My ideal region")
st.write("지역을 클릭 인구밀도를 확인해주세요")

# 지도 객체를 생성합니다.
m = folium.Map(location=[36, 127], zoom_start=6)

# GeoJSON 레이어를 지도에 추가하고 팝업 기능을 설정합니다.
folium.GeoJson(
    geo_data,
    name='geojson',
    style_function=lambda x: {'fillColor': '#ffffff00'},
    highlight_function=lambda x: {'weight':3, 'color':'blue'},
    tooltip=folium.GeoJsonTooltip(fields=['CTP_KOR_NM']),
    popup=folium.GeoJsonPopup(fields=['website'], labels=False, parse_html = True)
).add_to(m)

# 지도를 표시합니다.
st_folium(m, width=700, height=500)