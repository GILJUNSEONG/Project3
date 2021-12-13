import pandas as pd
from myfunction import get_df

# conn, cur = init_db()

# area_code_list = {'종로구' : '11110', '중구' : '11140', '용산구' : '11170', '성동구' : '11200', '광진구' : '11215', '동대문구' : '11230', '중랑구' : '11260', '성북구' : '11290', '강북구' : '11305',
#                 '도봉구' : '11320', '노원구' : '11350', '은평구' : '11380', '서대문구' : '11410', '마포구' : '11440', '양천구' : '11470', '강서구' : '11500', '구로구' : '11530', '금천구' : '11545',
#                 '영등포구' : '11560', '동작구' : '11590', '관악구' : '11620', '서초구' : '11650', '강남구' : '11680', '송파구' : '11710', '강동구' : '11740'}

# df_origin = pd.DataFrame()
# for area_name, _ in area_code_list.items():
#     globals()[area_name] = get_data_db(area_name, conn, cur)
#     df_origin = df_origin.append(globals()[area_name])


from sklearn.ensemble import RandomForestRegressor
from category_encoders import OrdinalEncoder
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# df_origin = df_origin.dropna() # 결측치 제거
# df_origin = df_origin.reset_index(drop=True)

# apartment_name = df_origin['아파트']

# df_origin[['건축년도', '년', '지역코드', '월', '일', '층']] = df_origin[['건축년도', '년', '지역코드', '월','일', '층']].astype(int)
# df_origin['거래금액'] = df_origin['거래금액'].replace(',','', regex=True).astype(int)
# df_origin['전용면적'] = df_origin['전용면적'].astype(float)  # feature의 type을 알맞게 변경
# df = df_origin.drop(['아파트', '월', '일'], axis = 1) # 학습에 사용하지 않을 Feature 제거

# to_db(df_origin, 'all', conn, cur)

# df[['건축년도', '년', '지역코드', '월', '일', '층']] = df[['건축년도', '년', '지역코드', '월','일', '층']].astype(int)
# df['거래금액'] = df['거래금액'].replace(',','', regex=True).astype(int)
# df['전용면적'] = df['전용면적'].astype(float)  # feature의 type을 알맞게 변경

df, _ = get_df()

target = df['거래금액']
feature = df.drop(['거래금액'], axis=1)



# Hold-Out Validation 사용

X_train, X_test, y_train, y_test = train_test_split(feature, target, test_size=0.2, random_state=10) # test, train 분류
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=10) # train, validation 분류

model = make_pipeline(
    OrdinalEncoder(),
    RandomForestRegressor(n_estimators=96, max_features=4, max_depth=26)
)

model.fit(X_train, y_train)

import pickle

with open('model/model.pkl', 'wb') as pickle_file:
    pickle.dump(model, pickle_file)