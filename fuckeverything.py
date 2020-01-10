import copy
import time
from threading import Lock
from conf.constant import SEAT_TYPE, CAPTCHA_CHECK_METHOD_HAND
from configure import *
from net import init_ip_pool
from net.NetUtils import EasyHttp
from spider.get_free_proxy import GetFreeProxy
from train.login.Login import Login
from train.query import check_user_login
from train.query.Query import Query
from train.submit.Submit import Submit
from utils import TrainUtils
from utils import Utils, deadline
from utils.Log import Log
from utils.email_tool import send_mail
from utils.sms import send_sms

def do_login(love):
    EasyHttp.removeCookies()
    login = Login()
    Log.v('正在登录...')
    result, msg = login.login(USER_NAME, USER_PWD, SELECT_AUTO_CHECK_CAPTHCA)
    EasyHttp.save_cookies(COOKIE_SAVE_ADDRESS)
    if not Utils.check(result, msg):
        return False,login
    Log.v('%s,登录成功' % msg)
    love.change_login_status(True)
    return True,login

def super_hero(love):
    Log.v('启动***超级英雄***线程')
    #免费代理ip访问
    GetFreeProxy.getAllProxy(THREAD_POOL_SIZE, THREAD_OR_PROCESS, IS_REFASH_IP_POOL)
    init_ip_pool()

    EasyHttp.load_cookies(COOKIE_SAVE_ADDRESS)
    cookies = {c.name: c.value for c in EasyHttp.get_session().cookies}

    if 'uamtk' not in cookies or 'RAIL_DEVICEID' not in cookies:
        status,login = do_login(love)
        if not status:
            love.change_offline_status(True)
            return
    else:
        status,_ = check_user_login()
        if not status:
            status, login = do_login(love)
            if not status:
                love.change_offline_status(True)
                return

        Log.v('已登录状态,开始寻找小票票')

    seatTypesCode = SEAT_TYPE_CODE if SEAT_TYPE_CODE else [SEAT_TYPE[key] for key in SEAT_TYPE.keys()]
    passengerTypeCode = PASSENGER_TYPE_CODE if PASSENGER_TYPE_CODE else '1'
    Log.d("配置详情:日期[%s]/区间[%s至%s]%s%s/刷票间隔[%ss]"%(','.join(TRAIN_DATE),FROM_STATION,TO_STATION,'/出发时间段['+'~'.join(leave_time)+']' if leave_time else '','/车次['+','.join(TRAINS_NO)+']' if TRAINS_NO else '',QUERY_TICKET_REFERSH_INTERVAL))
    count = 0
    while True:
        try:
            nowTime, status = deadline.do_fix_time()
            if status:
                Log.v('当前时间:%s 处于23点到6点之间，12306处于维护状态，暂不处理下单业务' % nowTime)
                continue

            count += 1
            Log.v('第%d次访问12306网站' % count)
            print('-' * 40)
            ticketDetails = Query.loopQuery(TRAIN_DATE, FROM_STATION, TO_STATION,
                                            TrainUtils.passengerType2Desc(passengerTypeCode),
                                            TRAINS_NO,
                                            seatTypesCode, PASSENGERS_ID,leave_time, POLICY_BILL, QUERY_TICKET_REFERSH_INTERVAL)
            status = love.get_login_status()
            # status,_ = check_user_login()
            if not status:
                #非登录状态有票,仅支持自动登录或第三方AI自动登录
                if SELECT_AUTO_CHECK_CAPTHCA == CAPTCHA_CHECK_METHOD_HAND:
                    Log.e("手动模式登录状态已过期,请手动重试...")

                status, login = do_login(love)
                if not status:
                    Log.e("登录状态已过期,重试登录失败")
                    love.change_offline_status(True)
                    return

            # Log.v('已为您查询到可用余票:%s' % ticketDetails)
            Log.v('已为您查询到可用余票:[日期:%s,车次:%s,出发站:%s,到达站:%s,出发时间:%s,到达时间:%s]' % (ticketDetails.custom_date,ticketDetails.trainNo,ticketDetails.fromStation,ticketDetails.toStation,ticketDetails.leaveTime,ticketDetails.arriveTime))

            ticketDetails.passengersId = PASSENGERS_ID
            ticketDetails.ticketTypeCodes = passengerTypeCode
            ticketDetails.tourFlag = TOUR_FLAG if TOUR_FLAG else 'dc'
            submit = Submit(ticketDetails)
            seats_default = copy.deepcopy(CHOOSE_SEATS)
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
    love.change_offline_status(True)

def girl_of_the_night(love):
    Log.v('启动***休眠监控***线程')
    while 1:
        if love.get_my_love():
            break
        if love.get_login_status():
            status,_ = check_user_login()
            if status:
                EasyHttp.save_cookies(COOKIE_SAVE_ADDRESS)
            else:
                love.change_login_status(False)
        time.sleep(HEART_BEAT_PER_REQUEST_TIME)

    Log.v('****** 12306 终止 ******')

def start_service(love):
    import threadpool
    pool = threadpool.ThreadPool(2)
    reqs = threadpool.makeRequests(super_hero, [love])
    [pool.putRequest(req) for req in reqs]
    reqs = threadpool.makeRequests(girl_of_the_night, [love])
    [pool.putRequest(req) for req in reqs]
    pool.wait()

class Love():
    def __init__(self,love,hero,is_login):
        self.love = love
        self.hero = hero
        self.is_login = is_login

    def change_offline_status(self,status):
        self.hero.acquire()
        self.love = status
        self.hero.release()

    def change_login_status(self,status):
        self.hero.acquire()
        self.is_login = status
        self.hero.release()

    def get_my_love(self):
        return self.love

    def get_login_status(self):
        return self.is_login

if __name__ == '__main__':
    Log.v('****** 12306 启动 ******')
    love = Love(False,Lock(),False)
    start_service(love)