import collections
import datetime
import time

from colorama import Fore
from prettytable import PrettyTable

from conf.city_code import city2code, code2city
from conf.constant import PASSENGER_TYPE_ADULT, SEAT_TYPE
from conf.constant import POLICY_BILL_ALL
from conf.urls_conf import queryUrls
from configure import QUERY_TICKET_REFERSH_INTERVAL
from net.NetUtils import EasyHttp
from train.TicketDetails import TicketDetails
from utils import TrainUtils, deadline
from utils.Log import Log

#  车次：3
INDEX_TRAIN_NO = 3
#  start_station_code:起始站：4
INDEX_TRAIN_START_STATION_CODE = 4
#  end_station_code终点站：5
INDEX_TRAIN_END_STATION_CODE = 5
#  from_station_code:出发站：6
INDEX_TRAIN_FROM_STATION_CODE = 6
#  to_station_code:到达站：7
INDEX_TRAIN_TO_STATION_CODE = 7
#  start_time:出发时间：8
INDEX_TRAIN_LEAVE_TIME = 8
#  arrive_time:达到时间：9
INDEX_TRAIN_ARRIVE_TIME = 9
#  历时：10
INDEX_TRAIN_TOTAL_CONSUME = 10
#  商务特等座：32
INDEX_TRAIN_BUSINESS_SEAT = 32
#  一等座：31
INDEX_TRAIN_FIRST_CLASS_SEAT = 31
#  二等座：30
INDEX_TRAIN_SECOND_CLASS_SEAT = 30
#  高级软卧：21
INDEX_TRAIN_ADVANCED_SOFT_SLEEP = 21
#  软卧：23
INDEX_TRAIN_SOFT_SLEEP = 23
#  动卧：33
INDEX_TRAIN_MOVE_SLEEP = 33
#  硬卧：28
INDEX_TRAIN_HARD_SLEEP = 28
#  软座：24
INDEX_TRAIN_SOFT_SEAT = 24
#  硬座：29
INDEX_TRAIN_HARD_SEAT = 29
#  无座：26
INDEX_TRAIN_NO_SEAT = 28
#  其他：22
INDEX_TRAIN_OTHER = 22
#  备注：1
INDEX_TRAIN_MARK = 1

INDEX_SECRET_STR = 0

INDEX_START_DATE = 13  # 车票出发日期


#
#  start_train_date:车票出发日期：13

class Query(object):
    @staticmethod
    def query(flag, base_url, trainDate, fromStation, toStation, passengerType=PASSENGER_TYPE_ADULT):
        # params = {
        #     r'leftTicketDTO.train_date': trainDate,
        #     r'leftTicketDTO.from_station': city2code(fromStation),
        #     r'leftTicketDTO.to_station': city2code(toStation),
        #     r'purpose_codes': passengerType
        # }
        params = collections.OrderedDict()
        params['leftTicketDTO.train_date'] = trainDate
        params['leftTicketDTO.from_station'] = city2code(fromStation)
        params['leftTicketDTO.to_station'] = city2code(toStation)
        params['purpose_codes'] = passengerType

        if flag > 1:
            jsonRet = EasyHttp.send(queryUrls['query'], params=params)
        else:
            for suffix in ['', 'O', 'X', 'Z', 'A', 'T', 'V']:
                queryUrls['query']['url'] = base_url + suffix
                jsonRet = EasyHttp.send(queryUrls['query'], params=params)
                if jsonRet:
                    break
        try:
            if jsonRet:
                return Query.__decode(jsonRet['data']['result'], passengerType)
        except Exception as e:
            Log.e(e)

        return []

    @staticmethod
    def __decode(queryResults, passengerType):
        for queryResult in queryResults:
            info = queryResult.split('|')
            ticket = TicketDetails()
            ticket.passengerType = passengerType
            ticket.trainNo = info[INDEX_TRAIN_NO]
            ticket.startStationCode = info[INDEX_TRAIN_START_STATION_CODE]
            ticket.endStationCode = info[INDEX_TRAIN_END_STATION_CODE]
            ticket.fromStationCode = info[INDEX_TRAIN_FROM_STATION_CODE]
            ticket.toStationCode = info[INDEX_TRAIN_TO_STATION_CODE]
            ticket.leaveTime = info[INDEX_TRAIN_LEAVE_TIME]
            ticket.arriveTime = info[INDEX_TRAIN_ARRIVE_TIME]
            ticket.totalConsume = info[INDEX_TRAIN_TOTAL_CONSUME]
            ticket.businessSeat = info[INDEX_TRAIN_BUSINESS_SEAT]
            ticket.firstClassSeat = info[INDEX_TRAIN_FIRST_CLASS_SEAT]
            ticket.secondClassSeat = info[INDEX_TRAIN_SECOND_CLASS_SEAT]
            ticket.advancedSoftSleep = info[INDEX_TRAIN_ADVANCED_SOFT_SLEEP]
            ticket.softSleep = info[INDEX_TRAIN_SOFT_SLEEP]
            ticket.moveSleep = info[INDEX_TRAIN_MOVE_SLEEP]
            ticket.hardSleep = info[INDEX_TRAIN_HARD_SLEEP]
            ticket.softSeat = info[INDEX_TRAIN_SOFT_SEAT]
            ticket.hardSeat = info[INDEX_TRAIN_HARD_SEAT]
            ticket.noSeat = info[INDEX_TRAIN_NO_SEAT]
            ticket.other = info[INDEX_TRAIN_OTHER]
            ticket.mark = info[INDEX_TRAIN_MARK]
            ticket.startStation = code2city(ticket.startStationCode)
            ticket.endStation = code2city(ticket.endStationCode)
            ticket.fromStation = code2city(ticket.fromStationCode)
            ticket.toStation = code2city(ticket.toStationCode)
            ticket.secretStr = info[INDEX_SECRET_STR]
            ticket.startDate = info[INDEX_START_DATE]
            yield ticket

    @staticmethod
    def outputPretty(trainDate, fromStation, toStation, passengerType=PASSENGER_TYPE_ADULT):
        table = PrettyTable()
        base_query_url = queryUrls['query']['url']
        table.field_names = '车次 车站 时间 历时 商务特等座 一等座 二等座 高级软卧 软卧 动卧 硬卧 软座 硬座 无座 其他 备注'.split(sep=' ')
        for ticket in Query.query(1, base_query_url, trainDate, fromStation, toStation, passengerType):
            if not ticket:
                continue
            table.add_row([ticket.trainNo,
                           '\n'.join([Fore.GREEN + ticket.fromStation + Fore.RESET,
                                      Fore.RED + ticket.toStation + Fore.RESET]),
                           '\n'.join(
                               [Fore.GREEN + ticket.leaveTime + Fore.RESET,
                                Fore.RED + ticket.arriveTime + Fore.RESET]),
                           ticket.totalConsume,
                           ticket.businessSeat or '--',
                           ticket.firstClassSeat or '--',
                           ticket.secondClassSeat or '--',
                           ticket.advancedSoftSleep or '--',
                           ticket.softSleep or '--',
                           ticket.moveSleep or '--',
                           ticket.hardSleep or '--',
                           ticket.softSeat or '--',
                           ticket.hardSeat or '--',
                           ticket.noSeat or '--',
                           ticket.other or '--',
                           ticket.mark or '--']
                          )
        print(table)

    @staticmethod
    def querySpec(flag, base_url, trainDate, fromStation, toStation, passengerType=PASSENGER_TYPE_ADULT, trainsNo=[],
                  seatTypes=[SEAT_TYPE[key] for key in SEAT_TYPE], PASSENGERS_ID=[],leave_period=[], POLICY_BILL=1):
        for custom_date in trainDate:
            for ticket in Query.query(flag, base_url, custom_date, fromStation, toStation, passengerType):
                if '售' in ticket.mark:
                    continue
                # filter trainNo
                if not TrainUtils.filterTrain(ticket, trainsNo):
                    continue
                # filter leave time
                try:
                    if leave_period and (ticket.leaveTime < leave_period[0] or ticket.leaveTime > leave_period[1]):
                        continue
                except Exception as e:
                    pass
                # filter seat
                for seatTypeName, seatTypeProperty in TrainUtils.seatWhich(seatTypes, ticket):
                    if seatTypeProperty and seatTypeProperty != '无':
                        Log.v('%s %s %s: %s' % (custom_date, ticket.trainNo, seatTypeName, seatTypeProperty))
                        try:
                            remind_num = int(seatTypeProperty)
                        except Exception as e:
                            remind_num = 100
                        if POLICY_BILL == POLICY_BILL_ALL and len(PASSENGERS_ID) > remind_num:
                            break
                        ticket.seatType = SEAT_TYPE[seatTypeName]
                        ticket.remindNum = remind_num
                        ticket.custom_date = custom_date
                        yield ticket
        return []

    @staticmethod
    def loopQuery(trainDate, fromStation, toStation, passengerType=PASSENGER_TYPE_ADULT, trainsNo=[],
                  seatTypes=[SEAT_TYPE[key] for key in SEAT_TYPE], PASSENGERS_ID=[],leave_period=[], POLICY_BILL=1,
                  timeInterval=QUERY_TICKET_REFERSH_INTERVAL):
        count = 0
        base_query_url = queryUrls['query']['url']
        while True:
            nowTime, status = deadline.do_fix_time()
            if status:
                Log.v('当前时间:%s 处于23点到6点之间，12306处于维护状态，暂不处理下单业务' % nowTime)
                continue

            count += 1
            Log.v('正在为您第%d次刷票' % count + '，当前时间为:%s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            for ticketDetails in Query.querySpec(count, base_query_url, trainDate, fromStation, toStation,
                                                 passengerType, trainsNo, seatTypes,
                                                 PASSENGERS_ID,leave_period, POLICY_BILL):
                if ticketDetails:
                    return ticketDetails
            time.sleep(timeInterval)

if __name__ == "__main__":
    # for ticket in Query.query('2017-12-31', '深圳北', '潮汕'):
    #     print(ticket)
    Query.outputPretty('2019-06-01', '沙坪坝', '兰州')
