import json

import streamlit as st
from openai import OpenAI

from trained_rfc_model import TrainedRfcModel
from user import User

# 노출 금지.
api_key = ""
client = OpenAI(api_key=api_key)


# 예측 모델 함수 (가정: 이미 3개 지역을 예측하는 모델이 존재)
def predict_top_3_regions(user_info: User):
    return TrainedRfcModel().predict_top_3_regions(user_info)


# 방문지 정보 요청 함수 (사용자 정보 추가)
def request_region_info(region_name, user_info) -> dict:
    prompt = f"""
    방문지 정보: {region_name} 
    사용자 정보: {user_info}
    방문지 정보를 포함한 dataframe 정보와 사용자 dictionary 정보를 전달할께.
    거주지 기준 방문지까지 거리와 교통편, 방문지 근처 유명한 관광명소, 방문지를 포함한 여행 일정, 여행 일정에 따른 예상 비용을 응답 형식에 맞춰서 json으로 제공해줘. 
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """
            너는 여행 정보 전문가야. 입력된 방문지과 여행객 정보를 제공할께. 다음 응답형식에 맞춰서 json 형태로 맞춤형 정보를 제공 해줘.
            방문지 정보: 방문지이름, 도로명주소, 경도, 위도
            사용자 정보: 성별, 연령대, 동반인원수, 거주지, 여행유형, 여행기간
            응답형식 : {'교통', '명소', '일정', '비용'}
            """},
            {"role": "user", "content": prompt}
        ]
    )
    result = response.choices[0].message.content
    print(result)

    return json.loads(result)

# 메인 공간
st.set_page_config(page_title="국내 여행지 추천", page_icon="✈️", layout="wide")  # 페이지 설정
st.title("✨ 나만의 맞춤 여행지 찾기 ✨")
st.markdown("##### 당신에게 딱 맞는 국내 여행지를 추천해드립니다! 🏖️⛰️")  # 제목 스타일 변경

# 사용자 정보 입력 섹션 (필터 기능 추가)
with st.form("여행 정보 입력"):
    st.write("🤔 여행 정보를 입력해주세요!")
    col1, col2 = st.columns(2)

    with col1: 
        GENDER = st.selectbox('성별', ('남', '여'))
        AGE_GRP = st.selectbox('귀하의 연령대는 어떻게 되십니까?',(
                                    # "~9세이하",
                                    # "10대",
                                    "20대",
                                    "30대",
                                    "40대",
                                    "50대",
                                    "60대",
                                    # "70세 이상"
        ))#연령대
        RESIDENCE_SGG_CODE = st.selectbox('거주지',('경기도', '대전광역시', '서울특별시', '대구광역시', '경상북도', '인천광역시', '충청북도', '충청남도', '전라북도', '강원도', '광주광역시', '제주특별자치도', '울산광역시', '부산광역시', '전라남도', '세종특별자치시', '경상남도'))

    with col2: 
        REL_CD = st.selectbox('어떤 여행입니까?',('2인 가족 여행', '나홀로 여행', '자녀 동반 여행', '2인 여행(가족 외)', '3인 이상 여행(가족 외)', '부모 동반 여행', '3대 동반 여행(친척 포함)', '3인 이상 가족 여행(친척 포함)'))
        TRAVEL_COMPANIONS_NUM = st.text_input('여행 동반자 수',placeholder="1,2,3....")
        days = st.text_input('여행기간',placeholder="1,2,3...")

    submitted = st.form_submit_button("✈️ 추천 여행지 찾기!")

if submitted:
    user_info = User(GENDER, AGE_GRP, TRAVEL_COMPANIONS_NUM, RESIDENCE_SGG_CODE, REL_CD, days)

    # 예측 모델을 통해 만족도 높은 방문지 3개 예측 (가정된 예측 모델 사용)
    top_3_place_df = predict_top_3_regions(user_info)

    # 각 방문지에 대한 정보 API 요청 및 출력 (사용자 정보 추가)
    for place in top_3_place_df.itertuples():
        place_name = place.방문지이름
        place_address = place.도로명주소
        place_lat = place.위도
        place_lon = place.경도

        # 방문지별 이미지 추가 (Unsplash API 활용)
        # 해당 url 이미지 가져올 수 없어서 주석처리.
        # st.image(f"https://source.unsplash.com/random/800x600/?{place_name},Korea", use_column_width=True, caption=place_name)

        st.markdown(f"## 🤩 {place_name}({place_address})")

        region_info = request_region_info(place_name, user_info)

        # 정보를 탭으로 구분하여 표시
        try:
            tab1, tab2, tab3, tab4 = st.tabs(["✨ 교통", "🏨 명소", "🍽️ 일정", "🍽️ 비용"])
            with tab1:
                st.write(region_info.get('교통', '정보 없음'))
            with tab2:
                st.write(region_info.get('명소', '정보 없음'))
            with tab3:
                st.write(region_info.get('일정', '정보 없음'))
            with tab4:
                st.write(region_info.get('비용', '정보 없음'))

        except IndexError:
            st.warning("API 응답 형식이 예상과 다릅니다. 정보를 탭으로 구분하여 표시할 수 없습니다.")
            st.write(region_info)

