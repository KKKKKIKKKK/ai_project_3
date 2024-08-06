import streamlit as st
from openai import OpenAI

api_key =""


client = OpenAI(api_key=api_key)
# 결과 구성
def tourgpt(prompt, api_key):
    # gpt에게 질문하면 response에 답변이 저장됨
    response = client.chat.completions.create(
        model="gpt-4o", 
        messages=[
            {"role":"system","content":"""""
             너는 최고의여행지추천전문가야.입력된 정보에 기반해 여행지를 추천해줘
             답변양식  :
             1. 추천여행지 : 
             2. 서울에서 걸리는 시간:
             3. 추천하는 일정(예상 비용) :
             4. 추천 여행지 사진 : """},
            {"role":"user","content":prompt}
        ]
    )
    result =  response.choices[0].message.content
    # print(result)
    return result


# input부분
st.header(":blue[맞춤형 여행] 추천 프로그램 :sunglasses:")
st.markdown("---")
st.image(r"C:\Users\user\Desktop\test\img_rec.png", caption="Vamos!")


import streamlit as st

col1, col2, col3 = st.columns(3)

with col1: 
    GENDER = st.text_input('성별',placeholder="남/여")
    AGE_GRP = st.selectbox('귀하의 연령대는 어떻게 되십니까?',(
                                   "~9세이하",
                                   "10대",
                                   "20대",
                                   "30대",
                                   "40대",
                                   "50대",
                                   "60대",
                                   "70세 이상"))#연령대
    RESIDENCE_SGG_CODE = st.selectbox('거주지',("서울","인천","경기","강원","대구","경북","부산","울산","경남","광주","전북","전남","대전","충북","충남","세종","제주","도서지역"))

with col2: 
    REL_CD = st.selectbox('동반자와의 관계는?',("배우자","자녀",'부모','형제/자매','친인척','친구','연인','동료','친목 단체/모임(동호회,종교단체 등)','기타'))#동반자  관계 코드 TCR
    TRAVEL_COMPANIONS_NUM = st.text_input('여행 동반자 수',placeholder="1,2,3....")
    days = st.text_input('여행기간',placeholder="1,2,3...")


if st.button("내게 맞는 여행지 추천"):
    prompt = f'''
    아래 내용을 참고해서 국내 여행지 및 일정을 추천해줘.
    - 성별 : {GENDER}
    - 연령대 :  {AGE_GRP}
    - 여행 동반자 수 : {TRAVEL_COMPANIONS_NUM}
    - 거주지 : {RESIDENCE_SGG_CODE}
    - 동반자 관계 : {REL_CD}
    - 여행 기간 : {days}
    '''

    st.info(tourgpt(prompt, api_key))
