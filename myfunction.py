def request_api(search_date, area_code):

    import requests

    url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev'
    service_key = 'oueQDVM2iC7uKx0/SSJkhdZ36kf9P7c3iFAM7a4PoccXNDax/LYaQFcjNZn47uF4Bu1vU1NRZLeGeY7MJFNZVQ=='

    params ={'serviceKey' : service_key, 'pageNo' : 1, 'numOfRows' : 1000, 'LAWD_CD' : area_code, 'DEAL_YMD' : search_date }

    response = requests.get(url, params=params)
    print(response)

    return response

def get_items(response):

    import xml.etree.ElementTree as ET

    root = ET.fromstring(response.content)
    item_list = []

    for child in root.find('body').find('items'):
        elements = child.findall('*')
        data = {}

        for element in elements:
            tag = element.tag.strip()
            text = element.text.strip()

            data[tag] = text
        
        item_list.append(data)

    return item_list

import sqlite3

def init_db():

    conn = sqlite3.connect('data/Deals_Apartments.db')
    cur = conn.cursor()

    return conn, cur

def to_db(df, table_name, conn, cur):

    df.to_sql(name=table_name, con=conn, if_exists='append')

    cur.close()

def get_data_db(table_name, conn, cur):
    
    import pandas as pd

    query = f"""SELECT 거래금액, 건축년도, 년, 월, 일, 법정동, 지역코드, 아파트, 전용면적, 층
                FROM {table_name}
                ORDER BY 년, 월, 일 ASC"""
    
    df = pd.read_sql_query(query, conn)

    cur.close()

    return df

def get_df():
    import pandas as pd
    conn, cur = init_db()

    area_code_list = {'종로구' : '11110', '중구' : '11140', '용산구' : '11170', '성동구' : '11200', '광진구' : '11215', '동대문구' : '11230', '중랑구' : '11260', '성북구' : '11290', '강북구' : '11305',
                '도봉구' : '11320', '노원구' : '11350', '은평구' : '11380', '서대문구' : '11410', '마포구' : '11440', '양천구' : '11470', '강서구' : '11500', '구로구' : '11530', '금천구' : '11545',
                '영등포구' : '11560', '동작구' : '11590', '관악구' : '11620', '서초구' : '11650', '강남구' : '11680', '송파구' : '11710', '강동구' : '11740'}

    df_origin = pd.DataFrame()
    for area_name, _ in area_code_list.items():
        globals()[area_name] = get_data_db(area_name, conn, cur)
        df_origin = df_origin.append(globals()[area_name])

    df_origin = df_origin.dropna() # 결측치 제거
    df_origin = df_origin.reset_index(drop=True)

    apartment_name = df_origin['아파트']

    df_origin[['건축년도', '년', '지역코드', '월', '일', '층']] = df_origin[['건축년도', '년', '지역코드', '월','일', '층']].astype(int)
    df_origin['거래금액'] = df_origin['거래금액'].replace(',','', regex=True).astype(int)
    df_origin['전용면적'] = df_origin['전용면적'].astype(float)  # feature의 type을 알맞게 변경
    df = df_origin.drop(['아파트', '월', '일'], axis = 1) # 학습에 사용하지 않을 Feature 제거

    return df, df_origin