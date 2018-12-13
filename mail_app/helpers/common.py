import datetime
from pandas.tseries.offsets import Day

def suffixDate():
    now_time = datetime.datetime.now()
    # 周一处理周五日期的（前三天）其它时间处理前一天的
    if now_time.weekday() == 0:
        date = (now_time - 3*Day()).strftime('%Y.%m.%-d')
    else:
        date = (now_time - 1*Day()).strftime('%Y.%m.%-d')
    return date

def formateDate():
    now_time = datetime.datetime.now()
    # 周一处理周五日期的（前三天）其它时间处理前一天的
    if now_time.weekday() == 0:
        date = (now_time - 3*Day()).strftime('%y%m%d')
    else:
        date = (now_time - 1*Day()).strftime('%y%m%d')
    return date