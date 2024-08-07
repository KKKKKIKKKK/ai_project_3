# 2-3(1차). 머신 러닝을 통한 맞춤형 여행 상품 추천 교육 실습 프로젝트

### 방문지 추천 시스템

#### package 구조
```
ai_project_3
├── README.md                                   : 프로젝트 설명
├── TL_csv                                      : 학습데이터
│  ├── tc_codeb_코드B.csv                        : 공통코드   
│  ├── tc_sgg_시군구코드.csv                       : 시군구코드
│  ├── tn_travel_여행_E.csv                      : 여행 데이터
│  ├── tn_traveller_master_여행객 Master_E.csv    : 여행객 데이터
│  └── tn_visit_area_info_방문지정보_E.csv         : 방문지 데이터
├── VL_csv                                      : 검증데이터
│  ├── tn_travel_여행_E.csv
│  ├── tn_traveller_master_여행객 Master_E.csv
│  └── tn_visit_area_info_방문지정보_E.csv
├── label_encoders.pkl                          : label encoders cache. 훈련 시 생성. 예측 시 재사용.
├── satisfaction_model.pkl                      : 훈련된 모델. 훈련 시 생성. 예측 시 재사용.
├── tour_ai_project.py                          : main program (streamlit + api)
├── train_rfc_model.py                          : 모델 훈련
├── trained_rfc_model.py                        : 훈련 모델 사용
└── user.py                                     : 여행객 정보 모델
```
