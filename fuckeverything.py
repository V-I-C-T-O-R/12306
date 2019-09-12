import copy
import datetime
import random
import time
from threading import Lock
from conf.constant import SEAT_TYPE, SeatName, NUM_SEAT, LETTER_SEAT, CAPTCHA_CHECK_METHOD_HAND
from conf.urls_conf import loginUrls
from configure import *
from net import init_ip_pool
from net.NetUtils import EasyHttp
from spider.get_free_proxy import GetFreeProxy
from train.login.Login import Login
from train.query import check_re_login
from train.query.Query import Query
from train.submit.Submit import Submit
from utils import TrainUtils
from utils import Utils, deadline
from utils.Log import Log
from utils.email_tool import send_mail
from utils.sms import send_sms

def do_login():
    EasyHttp.removeCookies()
    login = Login()
    Log.v('正在登录...')
    result, msg = login.login(USER_NAME, USER_PWD, SELECT_AUTO_CHECK_CAPTHCA)
    EasyHttp.save_cookies(COOKIE_SAVE_ADDRESS)
    if not Utils.check(result, msg):
        Log.e(msg)
        return False,login
    Log.v('%s,登录成功' % msg)
    return True,login

def check_login():
    response = EasyHttp.post_custom(loginUrls['normal']['conf'])
    if not response or not response.json():
        Log.d('登录状态检查失败,重新请求')
        status, login = do_login()
        if not status:
            return False
    resp = response.json()
    login_status = resp.get('data').get('is_login')
    Log.d('登录状态：%s' % login_status)
    if 'Y' != login_status:
        Log.d('登录状态已过期,重新请求')
        status, login = do_login()
        if not status:
            return False
    return True

def super_hero(love):
    Log.v('启动***超级英雄***线程')
    #免费代理ip访问
    GetFreeProxy.getAllProxy(THREAD_POOL_SIZE, THREAD_OR_PROCESS, IS_REFASH_IP_POOL)
    init_ip_pool()

    EasyHttp.load_cookies(COOKIE_SAVE_ADDRESS)
    cookies = {c.name: c.value for c in EasyHttp.get_session().cookies}

    RAIL_EXPIRATION = cookies.get('RAIL_EXPIRATION')
    #(int(RAIL_EXPIRATION)-172800000) < int(time.time()*1000)
    if RAIL_EXPIRATION and int(RAIL_EXPIRATION) < int(time.time()*1000) :
        Log.d('cookie登录已过期,重新请求')
        status,login = do_login()
        if not status:
            return
    else:
        if not ('uamtk' in cookies and 'RAIL_DEVICEID' in cookies):
            status,login = do_login()
            if not status:
                return
        else:
            status = check_login()
            if not status:
                return
            login = Login()
            login._urlInfo = loginUrls['normal']
            Log.v('已登录状态,开始寻找小票票')

    seatTypesCode = SEAT_TYPE_CODE if SEAT_TYPE_CODE else [SEAT_TYPE[key] for key in SEAT_TYPE.keys()]
    passengerTypeCode = PASSENGER_TYPE_CODE if PASSENGER_TYPE_CODE else '1'
    Log.d("订单详情:日期[%s]/区间[%s至%s]/车次[%s]/刷票间隔[%ss]"%(TRAIN_DATE,FROM_STATION,TO_STATION,','.join(TRAINS_NO),QUERY_TICKET_REFERSH_INTERVAL))
    count = 0
    while True:
        # 死循环一直查票，直到下单成功
        try:
            nowTime, status = deadline.do_fix_time()
            if status:
                Log.v('当前时间:%s 处于23点到6点之间，12306处于维护状态，暂不处理下单业务' % nowTime)
                continue

            count += 1
            Log.v('第%d次访问12306网站' % count)
            print('-' * 40)
            flag,ticketDetails = Query.loopQuery(TRAIN_DATE, FROM_STATION, TO_STATION,
                                            TrainUtils.passengerType2Desc(passengerTypeCode),
                                            TRAINS_NO,
                                            seatTypesCode, PASSENGERS_ID, POLICY_BILL, QUERY_TICKET_REFERSH_INTERVAL,HEART_BEAT_PER_REQUEST_TIME)
            #非登录状态有票,仅支持自动登录或第三方AI自动登录
            if not flag:
                if SELECT_AUTO_CHECK_CAPTHCA == CAPTCHA_CHECK_METHOD_HAND:
                    Log.e("手动验证模式登录重试失败,请手动重试")
                    return

                status, login = do_login()
                if not status:
                    Log.e("自动验证模式登录重试失败自动登录失败,请手动重试")
                    return

            Log.v('已为您查询到可用余票:%s' % ticketDetails)

            ticketDetails.passengersId = PASSENGERS_ID
            ticketDetails.ticketTypeCodes = passengerTypeCode
            ticketDetails.tourFlag = TOUR_FLAG if TOUR_FLAG else 'dc'
            submit = Submit(ticketDetails)
            seats_default = copy.deepcopy(CHOOSE_SEATS)
            if (ticketDetails.seatType == SEAT_TYPE[SeatName.FIRST_CLASS_SEAT] or ticketDetails.seatType == SEAT_TYPE[SeatName.SECOND_CLASS_SEAT]) and not seats_default:
                results_seat = []
                for i in range(len(PASSENGERS_ID)):
                    random_seat = random.choice(NUM_SEAT)+random.choice(LETTER_SEAT)
                    if random_seat in results_seat:
                        continue
                    results_seat.append(random_seat)
                seats_default.extend(results_seat)

            if submit.submit(seats_default):
                status, contents = submit.showSubmitInfoPretty()
                if status:
                    Log.v("获取车票详情成功")
                    flag = send_mail(mail_user, mailto_list, '12306订票结果通知', mail_host, mail_user, mail_pass, contents)
                    if flag:
                        Log.v("邮件发送成功!")
                    else:
                        Log.v("邮件发送失败!")

                sms_id = send_sms(ACCOUNT_SID,AUTO_TOKEN,FROM_NUM,TO_NUM,'小机机已经成功拿到小票票，请主人记得在30分钟内完成支付!!!')
                if sms_id:
                    Log.v("短信提醒发送成功!")
                else:
                    Log.v("短信提醒发送失败!")
                break
            time.sleep(1)
        except Exception as e:
            Log.w(e)
    login.loginOut()
    Log.d('注销登录成功')
    love.change_status(True)

def girl_of_the_night(love):
    Log.v('启动***休眠监控***线程')
    count = 0
    while 1:
        if love.get_my_love():
            break
        now = datetime.datetime.now()
        nowHour = now.hour
        if nowHour >= 23 or nowHour < 6:
            if count % HEART_BEAT_PER_REQUEST_TIME == 0:
                check_re_login()
            time.sleep(HEART_BEAT_PER_REQUEST_TIME >> 1)
            count +=1
            continue
        # Log.e('非23点-6点,休眠%s秒'%(HEART_BEAT_PER_REQUEST_TIME << 1))
        time.sleep(HEART_BEAT_PER_REQUEST_TIME << 1)

def start_service(love):
    import threadpool
    pool = threadpool.ThreadPool(2)
    reqs = threadpool.makeRequests(super_hero, [love])
    [pool.putRequest(req) for req in reqs]
    reqs = threadpool.makeRequests(girl_of_the_night, [love])
    [pool.putRequest(req) for req in reqs]
    pool.wait()

class Love():
    def __init__(self,love,hero):
        self.love = love
        self.hero = hero

    def change_status(self,status):
        self.hero.acquire()
        self.love = status
        self.hero.release()

    def get_my_love(self):
        return self.love

if __name__ == '__main__':
    love = Love(False,Lock())
    start_service(love)