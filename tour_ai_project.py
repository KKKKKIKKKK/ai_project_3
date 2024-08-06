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


# 지역 정보 요청 함수 (사용자 정보 추가)
def request_region_info(region_name, user_info):
    prompt = f"{region_name} 지역에 대한 필요한 정보를 알려줘. (추천 여행지, 숙박 정보, 주변 맛집, 그리고 주소들, 교통 정보, 예상 비용 등) 또한, 다음 사용자 정보를 고려하여 맞춤형 추천을 제공해줘: {user_info}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "너는 여행 정보 전문가야. 입력된 지역과 사용자 정보에 대한 필요한 정보를 제공하고, 사용자 맞춤형 추천을 해줘."},
            {"role": "user", "content": prompt}
        ]
    )
    result = response.choices[0].message.content
    return result

# 메인 공간
st.set_page_config(page_title="국내 여행지 추천", page_icon="✈️", layout="wide")  # 페이지 설정
st.title("✨ 나만의 맞춤 여행지 찾기 ✨")
st.markdown("##### 당신에게 딱 맞는 국내 여행지를 추천해드립니다! 🏖️⛰️")  # 제목 스타일 변경

# 사용자 정보 입력 섹션 (필터 기능 추가)
with st.form("여행 정보 입력"):
    st.write("🤔 여행 정보를 입력해주세요!")
    col1, col2 = st.columns(2)

    with col1: 
        GENDER = st.text_input('성별',placeholder="남/여")
        AGE_GRP = st.selectbox('귀하의 연령대는 어떻게 되십니까?',(
                                    "10대",
                                    "20대",
                                    "30대",
                                    "40대",
                                    "50대",
                                    "60대",
                                    "70세 이상"))#연령대
        RESIDENCE_SGG_CODE = st.selectbox('거주지',('경기도', '대전광역시', '서울특별시', '대구광역시', '경상북도', '인천광역시', '충청북도', '충청남도', '전라북도', '강원도', '광주광역시', '제주특별자치도', '울산광역시', '부산광역시', '전라남도', '세종특별자치시', '경상남도'))

    with col2: 
        REL_CD = st.selectbox('어떤 여행입니까?',('2인 가족 여행', '나홀로 여행', '자녀 동반 여행', '2인 여행(가족 외)', '3인 이상 여행(가족 외)', '부모 동반 여행', '3대 동반 여행(친척 포함)', '3인 이상 가족 여행(친척 포함)'))
        TRAVEL_COMPANIONS_NUM = st.text_input('여행 동반자 수',placeholder="1,2,3....")
        days = st.text_input('여행기간',placeholder="1,2,3...")

    submitted = st.form_submit_button("✈️ 추천 여행지 찾기!")

if submitted:
    user_info = User(GENDER, AGE_GRP, TRAVEL_COMPANIONS_NUM, RESIDENCE_SGG_CODE, REL_CD, days)

    # 예측 모델을 통해 만족도 높은 지역 3개 예측 (가정된 예측 모델 사용)
    top_3_regions_df = predict_top_3_regions(user_info)

    # 각 지역에 대한 정보 API 요청 및 출력 (사용자 정보 추가)
    for region in top_3_regions_df['VISIT_AREA_NM']:
        # 지역별 이미지 추가 (Unsplash API 활용)
        st.image(f"https://source.unsplash.com/random/800x600/?{region},Korea", use_column_width=True, caption=region) 

        st.markdown(f"## 🤩 {region}")
        region_info = request_region_info(region, user_info)

        # 정보를 탭으로 구분하여 표시
        try:
            info_sections = region_info.split("##")
            tab1, tab2, tab3 = st.tabs(["✨ 추천 여행지", "🏨 숙박", "🍽️ 맛집"])
            with tab1:
                st.write(info_sections[1].strip()) 
            with tab2:
                st.write(info_sections[2].strip()) 
            with tab3:
                st.write(info_sections[3].strip()) 
        except IndexError:
            st.warning("API 응답 형식이 예상과 다릅니다. 정보를 탭으로 구분하여 표시할 수 없습니다.")
            st.write(region_info)

