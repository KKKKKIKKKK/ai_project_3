import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# 코드B 데이터 불러오기
tc_codeb = pd.read_csv("TL_csv/tc_codeb_코드B.csv")

# 시군구코드 데이터 불러오기
tc_sgg = pd.read_csv("TL_csv/tc_sgg_시군구코드.csv")

# 여행객 파일 불러오기
df1 = pd.read_csv("TL_csv/tn_traveller_master_여행객 Master_E.csv")
df2 = pd.read_csv("VL_csv/tn_traveller_master_여행객 Master_E.csv")
tn_traveller_master = pd.concat([df1, df2])

# 성별: GENDER
# 나이: AGE_GRP (나이대 로 되어 있음)
# 인원: TRAVEL_COMPANIONS_NUM(동반인원)
# 거주지: TRAVEL_STATUS_RESIDENCE
# 여행현황_동반현황: TRAVEL_STATUS_ACCOMPANY
# 여행기간: tn_travel > DAYS 계산해서 추가
traveller_df = tn_traveller_master[ ['TRAVELER_ID', 'GENDER', 'AGE_GRP', 'TRAVEL_COMPANIONS_NUM', 'TRAVEL_STATUS_RESIDENCE', 'TRAVEL_STATUS_ACCOMPANY'] ]

# traveller_df의 AGE_GRP 값을 문자열로 변경하여 끝에 '대' 문자열 연결. 만약 값이 70이상이면 '70세이상', 10 미만이면 '~9세이하' 로 변경하여 'AGE' 컬럼에 저장
def convert_age(age):
    if age >= 70:
        return '70세이상'
    elif age < 10:
        return '~9세이하'
    else:
        return str(age) + '대'

traveller_df['AGE_GRP'] = traveller_df['AGE_GRP'].apply(convert_age)

# tn_travel_여행_E 파일 불러오기
df1 = pd.read_csv("TL_csv/tn_travel_여행_E.csv")
df2 = pd.read_csv("VL_csv/tn_travel_여행_E.csv")
tn_travel = pd.concat([df1, df2])

# 날짜 형식으로 변환
tn_travel['TRAVEL_START_YMD'] = pd.to_datetime(tn_travel['TRAVEL_START_YMD'])
tn_travel['TRAVEL_END_YMD'] = pd.to_datetime(tn_travel['TRAVEL_END_YMD'])

# 일수 계산
tn_travel['DAYS'] = (tn_travel['TRAVEL_END_YMD'] - tn_travel['TRAVEL_START_YMD']).dt.days

travel_df = tn_travel[ ['TRAVEL_ID', 'TRAVELER_ID', 'DAYS'] ]

# TRAVELER_ID 기준으로 traveller_df와 travel_df을 merge
travel_all_df = pd.merge(traveller_df, travel_df, on='TRAVELER_ID', how='left')

# tn_visit_area_info_방문지정보_E.csv
df1 = pd.read_csv("TL_csv/tn_visit_area_info_방문지정보_E.csv")
df2 = pd.read_csv("VL_csv/tn_visit_area_info_방문지정보_E.csv")
tn_visit_area_info = pd.concat([df1, df2])

# 필요 방문지 데이터 추출
visit_df = tn_visit_area_info[['TRAVEL_ID', 'VISIT_AREA_NM', 'DGSTFN']]

# tn_visit_area_info의 DGSTFN 컬럼 값이 Nan인 row 제거
visit_df = visit_df.dropna(subset=['DGSTFN'])

# 'VISIT_AREA_NM' 컬럼 값 모든 공백 제거
visit_df['VISIT_AREA_NM'] = visit_df['VISIT_AREA_NM'].str.replace(' ', '')

# TRAVEL_ID 기준으로 travel_all_df와 visit_df을 merge
all_df = pd.merge(travel_all_df, visit_df, on='TRAVEL_ID', how='left')

# 범주형 변수를 숫자로 변환
# 레이블 인코딩
label_encoders = {}
for column in ['GENDER', 'AGE_GRP', 'TRAVEL_STATUS_RESIDENCE', 'TRAVEL_STATUS_ACCOMPANY', 'VISIT_AREA_NM', 'DGSTFN']:
    le = LabelEncoder()
    all_df[column] = le.fit_transform(all_df[column])
    label_encoders[column] = le

# 레이블 인코더 저장
joblib.dump(label_encoders, 'label_encoders.pkl')
print("label_encoders saved as 'label_encoders.pkl'")

# 모델 학습
# 성별: GENDER
# 나이대: AGE_GRP
# 인원: TRAVEL_COMPANIONS_NUM(동반인원)
# 거주지: TRAVEL_STATUS_RESIDENCE
# 여행현황_동반현황: TRAVEL_STATUS_ACCOMPANY
# 여행기간: DAYS
# VISIT_AREA_NM: 방문지 명
# 만족도: DGSTFN
X = all_df[['GENDER', 'AGE_GRP', 'TRAVEL_COMPANIONS_NUM', 'TRAVEL_STATUS_RESIDENCE', 'TRAVEL_STATUS_ACCOMPANY', 'DAYS']]
y = all_df['VISIT_AREA_NM']
# y = all_df['DGSTFN']

# 가중치 설정 (만족도에 비례)
weights = all_df['DGSTFN']

# 데이터 분할
X_train, X_test, y_train, y_test, w_train, w_test = train_test_split(X, y, weights, test_size=0.2, random_state=42)

# 모델 학습
model = RandomForestClassifier(n_estimators=300, max_depth=12)
model.fit(X_train, y_train, sample_weight=w_train)

# 모델 예측 및 평가
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy}')

# 모델 저장
joblib.dump(model, 'satisfaction_model.pkl')
print("Model saved as 'satisfaction_model.pkl'")
