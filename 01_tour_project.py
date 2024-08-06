import streamlit as st
from openai import OpenAI

api_key = ""
client = OpenAI(api_key=api_key)

# 예측 모델 함수 (가정: 이미 3개 지역을 예측하는 모델이 존재)
def predict_top_3_regions(user_info):
    # 가정: user_info를 기반으로 만족도 높은 지역 3개를 예측하는 모델이 있다고 가정
    # 실제 구현 시에는 해당 모델을 호출하여 예측 결과를 반환해야 합니다.
    # 여기서는 간단한 규칙 기반 예측을 사용하여 예시를 보여줍니다.
    if "바다" in user_info:
        return ["부산", "강릉", "제주"]
    elif "산" in user_info:
        return ["강원도", "전라남도", "경상북도"]
    else:
        return ["서울", "제주", "부산"]

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
        age_options = ["0~10", "10~20", "20~30", "30~40", "40~50", "50~60", "60~70"]
        age = st.selectbox('나이', age_options)
        gender = st.selectbox('성별', ["남자", "여자"])
        home = st.selectbox('사는 곳', ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종", "경기도", "강원도", "충청북도", "충청남도", "전라북도", "전라남도", "경상북도", "경상남도", "제주도"])

    with col2:
        purpose = st.text_input('여행 목적', placeholder='호캉스, 피서, 워케이션...')
        person_num_options = [str(i) for i in range(11)]  # 0~10까지 숫자 리스트 생성
        person_num = st.selectbox('함께 가는 사람 수', person_num_options)
        days_options = [str(i) for i in range(1, 11)] + ["10일 이상"]
        days = st.selectbox('여행 일수', days_options)

    submitted = st.form_submit_button("✈️ 추천 여행지 찾기!")

if submitted:
    user_info = f''' 
    - 나이 : {age} 
    - 성별 : {gender} 
    - 사는 곳 : {home} 
    - 여행 목적 : {purpose} 
    - 함께 가는 사람 수 : {person_num} 
    - 여행 일수 : {days}
    '''

    # 예측 모델을 통해 만족도 높은 지역 3개 예측 (가정된 예측 모델 사용)
    top_3_regions = predict_top_3_regions(user_info)

    # 각 지역에 대한 정보 API 요청 및 출력 (사용자 정보 추가)
    for i, region in enumerate(top_3_regions):
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

        # 챗봇 기능 추가 (펼칠 수 있는 섹션 활용)
        with st.expander(f"🤖 {region} 챗봇에게 물어보기"):
            user_question = st.text_input("궁금한 점을 입력하세요:", key=f"chatbot_input_{region}")
            # 버튼에 고유한 key 값 할당
            if st.button("🙋‍♀️ 질문하기", key=f"chatbot_button_{i}"): 
                chatbot_prompt = f"{region} 지역에 대해 {user_question} 질문이 있어요. {user_info}를 참고해서 자세히 알려줄 수 있나요?"
                chatbot_response = request_region_info(region, chatbot_prompt)
                st.write(chatbot_response)
