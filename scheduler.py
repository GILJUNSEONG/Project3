from myfunction import request_api, get_items, drop_df, to_db, init_db
import apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

now = datetime.datetime.now()
today = "%s%s" %(now.year, now.month)

year = [str("%02d" %(y)) for y in range(2019, 2022)]
month = [str("%02d" %(m)) for m in range(1, 13)]
search_data_list = ["%s%s" %(y, m) for y in year for m in month]  # 2019~2021, 3년간의 데이터 수집

if today not in search_date_list:
    scheduler = BlockingScheduler({'apscheduler.timezone':'UTC'})
else:
    continue 