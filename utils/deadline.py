import datetime
import time

def do_fix_time():
    now = datetime.datetime.now()
    nowHour = now.hour
    nowTime = now.strftime('%Y-%m-%d %H:%M:%S')
    if nowHour >= 23 or nowHour < 6:
        time.sleep(60)
        return nowTime,True
    return None,False