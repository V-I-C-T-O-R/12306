import os
import time

from conf.constant import SEAT_TYPE
from configure import *
from net import init_ip_pool
from spider.get_free_proxy import GetFreeProxy
from train.login.Login import Login
from train.query.Query import Query
from train.submit.Submit import Submit
from utils import TrainUtils
from utils import Utils, deadline
from utils.Log import Log
from utils.email_tool import send_mail
from utils.sms import send_sms

address = os.path.dirname(os.path.realpath(__file__)) + '/'

def working(username=USER_NAME, password=USER_PWD, id_cards=PASSENGERS_ID, day=TRAIN_DATE, from_station=FROM_STATION,
            to_station=TO_STATION,
            seats=SEAT_TYPE_CODE, types=PASSENGER_TYPE_CODE, train_no=TRAINS_NO, polocy=POLICY_BILL,
            tour_flag=TOUR_FLAG, refersh=QUERY_TICKET_REFERSH_INTERVAL):
    GetFreeProxy.getAllProxy(THREAD_POOL_SIZE, THREAD_OR_PROCESS, IS_REFASH_IP_POOL)
    init_ip_pool()
    login = Login()
    Log.v('正在登录...')
    result, msg = login.login(username, password, SELECT_AUTO_CHECK_CAPTHCA)
    if not Utils.check(result, msg):
        Log.e(msg)
        return
    Log.v('%s,登录成功' % msg)

    seatTypesCode = seats if seats else [SEAT_TYPE[key] for key in SEAT_TYPE.keys()]
    passengerTypeCode = types if types else '1'

    count = 0
    while True:
        # 死循环一直查票，直到下单成功
        try:
            nowTime, status = deadline.do_fix_time()
            if status:
                Log.v('当前时间:%s 处于23点到6点之间，12306处于维护状态，暂不处理下单业务' % nowTime)
                continue

            count += 1
            Log.v('第%d 次访问12306网站' % count)
            print('-' * 40)
            ticketDetails = Query.loopQuery(day, from_station, to_station,
                                            TrainUtils.passengerType2Desc(passengerTypeCode),
                                            train_no,
                                            seatTypesCode, id_cards, polocy, refersh)
            Log.v('已为您查询到可用余票:%s' % ticketDetails)

            ticketDetails.passengersId = id_cards
            ticketDetails.ticketTypeCodes = passengerTypeCode
            ticketDetails.tourFlag = tour_flag if tour_flag else 'dc'
            submit = Submit(ticketDetails)
            if submit.submit(CHOOSE_SEATS):
                status, contents = submit.showSubmitInfoPretty()
                if status:
                    flag = send_mail(mail_user, mailto_list, '12306订票结果通知', mail_host, mail_user, mail_pass, contents)
                    if flag:
                        Log.v("邮件发送成功!")
                    else:
                        Log.v("邮件发送失败!")
                    sms_id = send_sms(ACCOUNT_SID, AUTO_TOKEN, FROM_NUM, TO_NUM, '小机机已经成功拿到小票票，请主人记得在30分钟内完成支付!!!')
                    if sms_id:
                        Log.v("短信提醒发送成功!")
                    else:
                        Log.v("短信提醒发送成功!")
                break
            time.sleep(1)
        except Exception as e:
            Log.w("提交操作异常：" + e)
    print(login.loginOut())

def main():
    GetFreeProxy.getAllProxy(THREAD_POOL_SIZE, THREAD_OR_PROCESS, IS_REFASH_IP_POOL)
    init_ip_pool()

    login = Login()
    Log.v('正在登录...')
    result, msg = login.login(USER_NAME, USER_PWD, SELECT_AUTO_CHECK_CAPTHCA)
    if not Utils.check(result, msg):
        Log.e(msg)
        return
    Log.v('%s,登录成功' % msg)

    seatTypesCode = SEAT_TYPE_CODE if SEAT_TYPE_CODE else [SEAT_TYPE[key] for key in SEAT_TYPE.keys()]
    passengerTypeCode = PASSENGER_TYPE_CODE if PASSENGER_TYPE_CODE else '1'

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
            ticketDetails = Query.loopQuery(TRAIN_DATE, FROM_STATION, TO_STATION,
                                            TrainUtils.passengerType2Desc(passengerTypeCode),
                                            TRAINS_NO,
                                            seatTypesCode, PASSENGERS_ID, POLICY_BILL, QUERY_TICKET_REFERSH_INTERVAL)
            Log.v('已为您查询到可用余票:%s' % ticketDetails)

            ticketDetails.passengersId = PASSENGERS_ID
            ticketDetails.ticketTypeCodes = passengerTypeCode
            ticketDetails.tourFlag = TOUR_FLAG if TOUR_FLAG else 'dc'
            submit = Submit(ticketDetails)
            if submit.submit(CHOOSE_SEATS):
                status, contents = submit.showSubmitInfoPretty()
                if status:
                    flag = send_mail(mail_user, mailto_list, '12306订票结果通知', mail_host, mail_user, mail_pass, contents)
                    if flag:
                        Log.v("邮件发送成功!")
                    else:
                        Log.v("邮件发送失败!")
                    sms_id = send_sms(ACCOUNT_SID,AUTO_TOKEN,FROM_NUM,TO_NUM,'小机机已经成功拿到小票票，请主人记得在30分钟内完成支付!!!')
                    if sms_id:
                        Log.v("短信提醒发送成功!")
                    else:
                        Log.v("短信提醒发送成功!")
                break
            time.sleep(1)
        except Exception as e:
            Log.w(e)
    print(login.loginOut())


if __name__ == '__main__':
    main()
