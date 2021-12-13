from myfunction import request_api, get_items, drop_df, to_db, init_db

import pandas as pd


year = [str("%02d" %(y)) for y in range(2019, 2022)]
month = [str("%02d" %(m)) for m in range(1, 13)]
search_data_list = ["%s%s" %(y, m) for y in year for m in month]  # 2019~2021, 3년간의 데이터 수집

area_code_list = {'종로구' : '11110', '중구' : '11140', '용산구' : '11170', '성동구' : '11200', '광진구' : '11215', '동대문구' : '11230', '중랑구' : '11260', '성북구' : '11290', '강북구' : '11305',
                '도봉구' : '11320', '노원구' : '11350', '은평구' : '11380', '서대문구' : '11410', '마포구' : '11440', '양천구' : '11470', '강서구' : '11500', '구로구' : '11530', '금천구' : '11545',
                '영등포구' : '11560', '동작구' : '11590', '관악구' : '11620', '서초구' : '11650', '강남구' : '11680', '송파구' : '11710', '강동구' : '11740'}

for area_name, area_code in area_code_list.items():
    items_list = []

    for search_data in search_data_list:
        response = request_api(search_data, area_code)
        items_list += get_items(response)

    items = pd.DataFrame(items_list)

    conn, cur = init_db()

    to_db(items, area_name, conn, cur)