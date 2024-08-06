import joblib
import numpy as np
import pandas as pd

from user import User


class TrainedRfcModel:
    
    def __init__(self):
        pass

    def predict(self, user: User):
            
        # 레이블 인코더 불러오기
        label_encoders = joblib.load('label_encoders.pkl')

        # 입력 데이터 변환
        input_data = user.to_dict()

        # 레이블 인코딩 수행
        for column, le in label_encoders.items():
            if column not in ['VISIT_AREA_NM', 'DGSTFN']:
                input_data[column] = le.transform([input_data[column]])[0]

        # 모델 불러오기
        model = joblib.load('satisfaction_model.pkl')

        # 예측 수행
        X_new = pd.DataFrame([input_data])
        predicted_proba = model.predict_proba(X_new)

        # 상위 3개 방문지 선택
        top_3_indices = np.argsort(predicted_proba[0])[::-1][:3]
        top_3_areas = label_encoders['VISIT_AREA_NM'].inverse_transform(top_3_indices)

        # 예측 결과 출력
        print(f'Top 3 visit areas based on predicted probabilities: {top_3_areas}')

        return top_3_areas

    @staticmethod
    def get_visit_area_info():

        # tn_visit_area_info_방문지정보_E.csv
        df1 = pd.read_csv("TL_csv/tn_visit_area_info_방문지정보_E.csv")
        df2 = pd.read_csv("VL_csv/tn_visit_area_info_방문지정보_E.csv")
        tn_visit_area_info = pd.concat([df1, df2])

        # 방문지 정보 중 필요한 정보만 슬라이싱하고 중복제거
        # VISIT_AREA_ID
        # VISIT_AREA_NM
        # ROAD_NM_ADDR
        # X_COORD
        # Y_COORD
        visit_df = tn_visit_area_info[['VISIT_AREA_NM', 'ROAD_NM_ADDR', 'X_COORD', 'Y_COORD']]

        # 'VISIT_AREA_NM' 컬럼 값 모든 공백 제거
        visit_df['VISIT_AREA_NM'] = visit_df['VISIT_AREA_NM'].str.replace(' ', '')

        # VISIT_AREA_NM 컬럼 중복 제거
        return visit_df.drop_duplicates(subset=['VISIT_AREA_NM'])

    def predict_top_3_regions(self, user: User):
        top_3 = self.predict(user)
        visit_df = self.get_visit_area_info()

        # 방문지 정보 조회
        visit_area_info = visit_df[visit_df['VISIT_AREA_NM'].isin(top_3)]
        print(visit_area_info)

        return visit_area_info


if __name__ == '__main__':
    TrainedRfcModel().predict_top_3_regions(User(
        '남',
        '20대',
        1,
        '서울특별시',
        '2인 여행(가족 외)',
        3)
    )
