class User:
    def __init__(self, gender, age_group, travel_companions_num, travel_status_residence, travel_status_accompany, days):
        self.gender = gender
        self.age_group = age_group
        self.travel_companions_num = travel_companions_num
        self.travel_status_residence = travel_status_residence
        self.travel_status_accompany = travel_status_accompany
        self.days = days

    def to_dict(self):
        return {
            'GENDER': self.gender,
            'AGE_GRP': self.age_group,
            'TRAVEL_COMPANIONS_NUM': self.travel_companions_num,
            'TRAVEL_STATUS_RESIDENCE': self.travel_status_residence,
            'TRAVEL_STATUS_ACCOMPANY': self.travel_status_accompany,
            'DAYS': self.days
        }
