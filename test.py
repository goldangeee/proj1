import streamlit as st
from streamlit_folium import st_folium
import folium
import json
import pandas as pd
import matplotlib.pyplot as plt
# import matplotlib.font_manager

# 대한민국 지도 경계 데이터를 불러옵니다.
with open("SIDO_MAP_2022_cp949.json", "r", encoding='cp949') as f:
    geo_data = json.load(f)

# 인구 밀도 데이터를 불러옵니다.
pop_den = pd.read_csv("pop_den.csv", encoding='utf-8') # 단위는 [명/km^2]

# 수평 막대 그래프, 히트맵
df1 = pd.DataFrame(pop_den)
df1_subset = df1[['행정구역별', '2022']]
df1_subset.drop(index=0, inplace=True)

plt.rcParams['font.family'] ='Malgun Gothic'

# 그래프를 그리기 위한 데이터 추출
x_values = df1_subset['2022']
y_values = df1_subset['행정구역별']
# 수평 막대 그래프 그리기
plt.barh(y_values, x_values)
# 그래프 제목 설정
plt.title('2022년 지역별 인구밀도')
# x축 레이블 설정
plt.xlabel('2022년 인구밀도[명/km^2]')
# y축 레이블 설정
plt.ylabel('지역')

# # 지역별 2022년 인구밀도 데이터
for feature in geo_data['features']:
    if feature['properties']['CTP_KOR_NM'] == '서울특별시':
        feature['properties']['DATA'] = str(pop_den.loc[pop_den["행정구역별"] == "서울특별시",'2022'].values[0])
    elif feature['properties']['CTP_KOR_NM'] == '부산광역시':
        feature['properties']['DATA'] = str(pop_den.loc[pop_den["행정구역별"] == "부산광역시",'2022'].values[0])
    elif feature['properties']['CTP_KOR_NM'] == '대구광역시':
        feature['properties']['DATA'] = str(pop_den.loc[pop_den["행정구역별"] == "대구광역시",'2022'].values[0])
    elif feature['properties']['CTP_KOR_NM'] == '인천광역시':
        feature['properties']['DATA'] = str(pop_den.loc[pop_den["행정구역별"] == "인천광역시",'2022'].values[0])
    elif feature['properties']['CTP_KOR_NM'] == '광주광역시':
        feature['properties']['DATA'] = str(pop_den.loc[pop_den["행정구역별"] == "광주광역시",'2022'].values[0])
    elif feature['properties']['CTP_KOR_NM'] == '대전광역시':
        feature['properties']['DATA'] = str(pop_den.loc[pop_den["행정구역별"] == "대전광역시",'2022'].values[0])
    elif feature['properties']['CTP_KOR_NM'] == '울산광역시':
        feature['properties']['DATA'] = str(pop_den.loc[pop_den["행정구역별"] == "울산광역시",'2022'].values[0])
    elif feature['properties']['CTP_KOR_NM'] == '세종특별자치시':
        feature['properties']['DATA'] = str(pop_den.loc[pop_den["행정구역별"] == "세종특별자치시",'2022'].values[0])
    elif feature['properties']['CTP_KOR_NM'] == '경기도':
        feature['properties']['DATA'] = str(pop_den.loc[pop_den["행정구역별"] == "경기도",'2022'].values[0])
    elif feature['properties']['CTP_KOR_NM'] == '강원도':
        feature['properties']['DATA'] = str(pop_den.loc[pop_den["행정구역별"] == "강원도",'2022'].values[0])
    elif feature['properties']['CTP_KOR_NM'] == '충청북도':
        feature['properties']['DATA'] = str(pop_den.loc[pop_den["행정구역별"] == "충청북도",'2022'].values[0])
    elif feature['properties']['CTP_KOR_NM'] == '충청남도':
        feature['properties']['DATA'] = str(pop_den.loc[pop_den["행정구역별"] == "충청남도",'2022'].values[0])
    elif feature['properties']['CTP_KOR_NM'] == '전라북도':
        feature['properties']['DATA'] = str(pop_den.loc[pop_den["행정구역별"] == "전라북도",'2022'].values[0])
    elif feature['properties']['CTP_KOR_NM'] == '전라남도':
        feature['properties']['DATA'] = str(pop_den.loc[pop_den["행정구역별"] == "전라남도",'2022'].values[0])
    elif feature['properties']['CTP_KOR_NM'] == '경상북도':
        feature['properties']['DATA'] = str(pop_den.loc[pop_den["행정구역별"] == "경상북도",'2022'].values[0])
    elif feature['properties']['CTP_KOR_NM'] == '경상남도':
        feature['properties']['DATA'] = str(pop_den.loc[pop_den["행정구역별"] == "경상남도",'2022'].values[0])
    elif feature['properties']['CTP_KOR_NM'] == '제주특별자치도':
        feature['properties']['DATA'] = str(pop_den.loc[pop_den["행정구역별"] == "제주특별자치도",'2022'].values[0])


# 상단에 타이틀과 설명을 배치합니다.
st.title("My ideal region")
st.write("지역을 클릭해서 지표를 확인해주세요")

# 화면을 두 부분으로 나눕니다.
col1, col2 = st.columns([1, 1])

# 첫 번째 컬럼(왼쪽)에 지도를 배치합니다.
with col1:
    # 지도 객체를 생성합니다.
    m = folium.Map(location=[36, 131.5], zoom_start=6.2)

    # GeoJSON 레이어를 지도에 추가하고 팝업 기능을 설정합니다.
    folium.GeoJson(
        geo_data,
        name='geojson',
        style_function=lambda x: {'fillColor': '#ffffff00'},
        highlight_function=lambda x: {'weight':3, 'color':'blue'},
        tooltip=folium.GeoJsonTooltip(fields=['CTP_KOR_NM']),
        popup=folium.GeoJsonPopup(fields=['DATA'], labels=False, parse_html=True)
    ).add_to(m)

    # 지도를 표시합니다.
    st_folium(m, width=700, height=500)

# 두 번째 컬럼(오른쪽)에는 도표를 배치할 수 있는 공간을 확보합니다.
with col2:
    st.write(st.pyplot(plt))

# 지역을 클릭하면 그 지역의 지표 순위들을 출력한다.
# 인구밀도 탭을 클릭하면 히트맵 표시