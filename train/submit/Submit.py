"""
下单
"""
import json
import re
import time
from datetime import datetime
import copy
import requests
from colorama import Fore

from conf.constant import TourFlag
from conf.urls_conf import submitUrls
from define.UserAgent import FIREFOX_USER_AGENT
from net import NetUtils
from net.NetUtils import EasyHttp
from train.query import check_user_login
from train.submit.PassengerDetails import PassengerDetails
from utils import TrainUtils
from utils import Utils
from utils.Log import Log


class Submit(object):
    def __init__(self, ticketDetails):
        self.__ticket = ticketDetails
        self._urlInfo = submitUrls['wc'] if self.__ticket.tourFlag == TourFlag.GO_BACK else \
            submitUrls['dc']

    # submit orher request,check if the orher is qualified
    def _submitOrderRequest(self, tourFlag='dc'):
        formData = {
            'secretStr': TrainUtils.undecodeSecretStr(self.__ticket.secretStr),
            # 'secretStr': self.__ticket.secretStr,
            # 'secretStr': urllib.parse.unquote(self.__ticket.secretStr),
            'train_date': Utils.formatDate(self.__ticket.startDate),  # 2018-01-04
            'back_train_date': time.strftime("%Y-%m-%d", time.localtime()),  # query date:2017-12-31
            'tour_flag': tourFlag,
            'purpose_codes': self.__ticket.passengerType,
            'query_from_station_name': self.__ticket.fromStation,
            'query_to_station_name': self.__ticket.toStation,
            'undefined': '',
        }
        order_request = copy.deepcopy(self._urlInfo['submitOrderRequest'])
        order_request['headers']['Referer'] = self._urlInfo['submitOrderRequest']['headers']['Referer']+ '?linktypeid='+tourFlag
        # jsonRet = EasyHttp.send(self._urlInfo['submitOrderRequest'], data=formData)
        response = EasyHttp.post_custom(order_request, data=formData)
        # print('submitOrderRequest %s' % jsonRet)
        if response and response.status_code == 302:
            self._urlInfo['submitOrderRequest']['url'] = response.headers['Location']
            response = EasyHttp.post_custom(self._urlInfo['submitOrderRequest'], data=formData)
        if response and response.status_code == requests.codes.ok:
            return True,'ok'
        return False,'failed'

    def _getExtraInfo(self):
        def getRepeatSubmitToken(html):
            repeatSubmitToken = re.findall(r"var globalRepeatSubmitToken = '(.*)'", html)[0]
            # print('RepeatSubmitToken = %s' % repeatSubmitToken)
            return repeatSubmitToken

        formData = {
            '_json_att': ''
        }
        extra_info = copy.deepcopy(self._urlInfo['getExtraInfo'])
        # extra_info['headers']['Referer'] = self._urlInfo['getExtraInfo']['headers']['Referer']+ '?linktypeid='+self.__ticket.tourFlag
        response = EasyHttp.post_custom(extra_info,data=formData)

        if response and response.status_code == requests.codes.ok:
            html = response.text
            if html.find('系统忙，请稍后重试') != -1:
                Log.e('系统忙，请稍后重试...')
                return False
        else:
            html = None
        # html = EasyHttp.send(self._urlInfo['getExtraInfo'])
        if not Utils.check(html, 'failed to visit %s' % self._urlInfo['getExtraInfo']['url']):
            return False
        self.__ticket.repeatSubmitToken = getRepeatSubmitToken(html)

        def decodeTicketInfoForPassengerForm(html):
            ticketInfoForPassengerForm = re.findall(r'var ticketInfoForPassengerForm=(.*);', html)[0]
            return json.loads(ticketInfoForPassengerForm.replace("'", "\""))
        # print('=======================')
        self.__ticket.ticketInfoForPassengerForm = decodeTicketInfoForPassengerForm(html)
        return True

    def __getPassengerInfo(self, passengersList):
        passengersDetails = {}
        for passengerJson in passengersList:
            passenger = PassengerDetails()
            passenger.passengerName = passengerJson.get('passenger_name') or ''
            passenger.code = passengerJson.get('code') or ''
            passenger.sexCode = passengerJson.get('sex_code') or ''
            passenger.sexName = passengerJson.get('sex_name') or ''
            passenger.bornDate = passengerJson.get('born_date') or ''
            passenger.countryCode = passengerJson.get('country_code') or ''
            passenger.passengerIdTypeCode = passengerJson.get('passenger_id_type_code') or ''
            passenger.passengerIdTypeName = passengerJson.get('passenger_id_type_name') or ''
            passenger.passengerIdNo = passengerJson.get('passenger_id_no') or ''
            passenger.passengerType = passengerJson.get('passenger_type') or ''
            passenger.passengerFlag = passengerJson.get('passenger_flag') or ''
            passenger.passengerTypeName = passengerJson.get('passenger_type_name') or ''
            passenger.mobileNo = passengerJson.get('mobile_no') or ''
            passenger.phoneNo = passengerJson.get('phone_no') or ''
            passenger.email = passengerJson.get('email') or ''
            passenger.address = passengerJson.get('address') or ''
            passenger.postalcode = passengerJson.get('postalcode') or ''
            passenger.firstLetter = passengerJson.get('first_letter') or ''
            passenger.recordCount = passengerJson.get('recordCount') or ''
            passenger.totalTimes = passengerJson.get('total_times') or ''
            passenger.indexId = passengerJson.get('index_id') or ''
            passenger.allEncStr = passengerJson.get('allEncStr') or ''

            #12306版本更新隐藏了证件号,直接取最后三位
            passengersDetails[passenger.passengerIdNo[-3:]] = passenger
            # passengersDetails[passenger.passengerIdNo] = passenger
        return passengersDetails

    # get user's passengers info
    def _getPassengerDTOs(self):
        if not self._getExtraInfo():
            return False, '获取乘客信息失败', None
        formData = {
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.__ticket.repeatSubmitToken,
        }
        jsonRet = EasyHttp.send(self._urlInfo['getPassengerDTOs'], data=formData)
        passengersList = jsonRet['data']['normal_passengers']
        return jsonRet['status'] if 'status' in jsonRet else False, \
               jsonRet['messages'] if jsonRet and 'messages' in jsonRet else '无法获取乘客信息，请先进行添加!', \
               self.__getPassengerInfo(passengersList)

    # passengerName:乘客姓名
    # seatType:座位类别（一等座，二等座····）
    # ticketTypeCodes:车票类别代码
    def _checkOrderInfo(self, passengersDetails, seatType, ticketTypeCodes=1):
        formData = {
            'cancel_flag': self.__ticket.ticketInfoForPassengerForm['orderRequestDTO']['cancel_flag'] or '2',
            'bed_level_order_num': self.__ticket.ticketInfoForPassengerForm['orderRequestDTO'][
                                       'bed_level_order_num'] or '000000000000000000000000000000',
            'passengerTicketStr': TrainUtils.passengerTicketStrs(seatType, passengersDetails, ticketTypeCodes),
            'oldPassengerStr': TrainUtils.oldPassengerStrs(passengersDetails),
            'tour_flag': self.__ticket.ticketInfoForPassengerForm['tour_flag'] or 'dc',
            'randCode': '',
            'whatsSelect': '1',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.__ticket.repeatSubmitToken,
        }
        jsonRet = EasyHttp.send(self._urlInfo['checkOrderInfo'], data=formData)
        submitStatus = ''
        errMsg = ''
        if jsonRet['data']:
            submitStatus = jsonRet['data']['submitStatus']
            errMsg = jsonRet['data']['errMsg'] if 'errMsg' in jsonRet['data'] else 'submit falied'
        return jsonRet['status'], jsonRet['messages'], submitStatus, errMsg

    def _getQueueCount(self):
        formData = {
            # Thu+Jan+04+2018+00:00:00+GMT+0800
            # 'train_date': datetime.strptime(
            #     self.__ticket.ticketInfoForPassengerForm['queryLeftTicketRequestDTO']['train_date'], '%Y%m%d').strftime(
            #     '%b+%a+%d+%Y+00:00:00+GMT+0800'),
            # Mon Jan 08 2018 00:00:00 GMT+0800 (中国标准时间)
            'train_date': datetime.strptime(
                self.__ticket.ticketInfoForPassengerForm['queryLeftTicketRequestDTO']['train_date'], '%Y%m%d').strftime(
                '%b %a %d %Y 00:00:00 GMT+0800') + ' (中国标准时间)',
            'train_no': self.__ticket.ticketInfoForPassengerForm['queryLeftTicketRequestDTO']['train_no'],
            'stationTrainCode': self.__ticket.trainNo,
            'seatType': self.__ticket.seatType,
            'fromStationTelecode': self.__ticket.fromStationCode,
            'toStationTelecode': self.__ticket.toStationCode,
            'leftTicket': self.__ticket.ticketInfoForPassengerForm['leftTicketStr'],
            'purpose_codes': self.__ticket.ticketInfoForPassengerForm['purpose_codes'],
            'train_location': self.__ticket.ticketInfoForPassengerForm['train_location'],
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.__ticket.repeatSubmitToken,
        }
        jsonRet = EasyHttp.send(self._urlInfo['getQueueCount'], data=formData)
        return jsonRet['status'], jsonRet['messages'], \
               jsonRet['data']['ticket'] if 'data' in jsonRet and 'ticket' in jsonRet['data'] else -1, \
               jsonRet['data']['count'] if 'data' in jsonRet and 'count' in jsonRet['data'] else -1

    # network busy usually occured
    def _confirmSingleOrGoForQueue(self, passengersDetails,choose_seat):
        formData = {
            'passengerTicketStr': TrainUtils.passengerTicketStrs(self.__ticket.seatType, passengersDetails,
                                                                 self.__ticket.ticketTypeCodes),
            'oldPassengerStr': TrainUtils.oldPassengerStrs(passengersDetails),
            'randCode': '',
            'purpose_codes': self.__ticket.ticketInfoForPassengerForm['purpose_codes'],
            'key_check_isChange': self.__ticket.ticketInfoForPassengerForm['key_check_isChange'],
            'leftTicketStr': self.__ticket.ticketInfoForPassengerForm['leftTicketStr'],
            'train_location': self.__ticket.ticketInfoForPassengerForm['train_location'],
            'choose_seats': ''.join(choose_seat) or '',
            # 'choose_seats':''.join(choose_seat) if choose_seat else '',
            'seatDetailType': '000',  # todo::make clear 000 comes from
            'whatsSelect': '1',
            'roomType': '00',  # todo::make clear this value comes from
            'dwAll': 'N',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.__ticket.repeatSubmitToken,
        }
        jsonRet = EasyHttp.send(self._urlInfo['confirmForQueue'], data=formData)
        return jsonRet['status'], jsonRet['messages'], jsonRet['data']['submitStatus'], jsonRet['data'][
            'errMsg'] if 'errMsg' in jsonRet['data'] else None

    def _queryOrderWaitTime(self):
        params = {
            'random': '%d' % (time.time() * 1000),
            'tourFlag': self.__ticket.ticketInfoForPassengerForm['tour_flag'] or 'dc',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.__ticket.repeatSubmitToken,
        }
        jsonRet = EasyHttp.send(self._urlInfo['queryOrderWaitTime'], params=params)

        return jsonRet['status'], jsonRet['messages'], jsonRet['data']['waitTime'], jsonRet['data']['orderId'], \
               jsonRet['data']['msg'] if 'msg' in jsonRet['data'] else None

    def _resultOrderForDcOrWcQueue(self, orderSequenceNo):
        formData = {
            'orderSequence_no': orderSequenceNo,
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.__ticket.repeatSubmitToken,
        }
        jsonRet = EasyHttp.send(self._urlInfo['resultOrderForQueue'], data=formData)
        # print('resultOrderForDcOrWcQueue', jsonRet)
        return jsonRet['status'], jsonRet['messages'], jsonRet['data']['submitStatus']

    # TODO::finish it
    def _payOrderInfo(self):
        url = r'https://kyfw.12306.cn/otn/payOrder/init?random=%d' % (time.time() * 1000)
        headers = {
            'User-Agent': FIREFOX_USER_AGENT,
            'Connection': 'keep-alive',
        }
        response = NetUtils.get(self.__session, url, headers=headers).text

    def _check_user(self,tourFlag = 'dc'):
        formData = {
            '_json_att': ''
        }
        check_user = copy.deepcopy(self._urlInfo['checkUser'])
        # check_user['headers']['Referer'] = self._urlInfo['checkUser']['headers']['Referer']+ '?linktypeid='+tourFlag
        jsonRet = EasyHttp.post_custom(check_user,data = formData)
        return True,jsonRet.text

    # seatType:商务座(9),特等座(P),一等座(M),二等座(O),高级软卧(6),软卧(4),硬卧(3),软座(2),硬座(1),无座(1)
    # ticket_type_codes:ticketInfoForPassengerForm['limitBuySeatTicketDTO']['ticket_type_codes']:(成人票:1,儿童票:2,学生票:3,残军票:4)
    def submit(self,choose_seat):
        # self._check_user(self.__ticket.tourFlag)
        # status,_ = check_user_login()
        # if not status:
        #     return False

        status, msg = self._submitOrderRequest(self.__ticket.tourFlag)
        if not Utils.check(status, 'submitOrderRequesst: %s' % msg):
            return False
        Log.v('提交订单请求成功!')

        status, msg, passengersDetailsList = self._getPassengerDTOs()
        if not Utils.check(status, 'getPassengerDTOs: %s' % msg):
            return False
        Log.v('获取乘客信息成功!')
        passengersDetails = []
        if len(self.__ticket.passengersId) >= self.__ticket.remindNum:
            for i in range(self.__ticket.remindNum):
                id = self.__ticket.passengersId[i]
                ticket_details = passengersDetailsList.get(id[-3:])
                ticket_details.passengerIdNo = id
                passengersDetails.append(ticket_details)
        else:
            for id in self.__ticket.passengersId:
                ticket_details = passengersDetailsList.get(id[-3:])
                ticket_details.passengerIdNo = id
                passengersDetails.append(ticket_details)

        # time.sleep(0.2)
        status, msg, submitStatus, errMsg = self._checkOrderInfo(passengersDetails, self.__ticket.seatType,
                                                                 self.__ticket.ticketTypeCodes)
        if not Utils.check(status, 'checkOrderInfo: %s' % msg) or not Utils.check(submitStatus,
                                                                                  'checkOrderInfo: %s' % errMsg):
            return False
        Log.v('校验订单信息成功!')

        status, msg, leftTickets, personsCount = self._getQueueCount()
        if not Utils.check(status, 'getQueueCount: %s' % msg):
            return False
        Log.v('%s 剩余车票:%s ,目前排队人数: %s' % (self.__ticket.trainNo, leftTickets, personsCount))
        status, msg, submitStatus, errMsg = self._confirmSingleOrGoForQueue(passengersDetails,choose_seat)
        if not Utils.check(status, 'confirmSingleOrGoForQueue: %s' % msg) \
                or not Utils.check(submitStatus, 'confirmSingleOrGoForQueue: %s' % errMsg or '订单信息提交失败！'):
            return False

        orderId = self.__waitForOrderId()
        if not Utils.check(orderId, '订单获取失败！'):
            return False

        status, msg, submitStatus = self._resultOrderForDcOrWcQueue(orderId)
        if not Utils.check(status, 'resultOrderForDcOrWcQueue: %s' % msg):
            return False
        if not submitStatus:
            Log.e('订单提交失败！')
            return False
        Log.v('您已成功订购火车票！请在30分钟内前往12306官方网站进行支付！')
        return True

    def _queryMyOrderNoComplete(self):
        formData = {
            '_json_att': '',
        }
        jsonRet = EasyHttp.send(self._urlInfo['queryMyOrderNoComplete'], data=formData)
        try:
            status = jsonRet['status']
            messages = jsonRet['messages']
            datas = jsonRet['data']
        except Exception as e:
            return False,None,None
        return status, messages, datas

    def showSubmitInfoPretty(self):
        status, msg, jsonTicketInfo = self._queryMyOrderNoComplete()
        if not Utils.check(status, msg):
            return False,msg
        from prettytable import PrettyTable
        table = PrettyTable()
        try:
            table.field_names = '序号 车次信息 席位信息 旅客信息 票款金额 车票状态'.split(sep=' ')
            totalTicketNum = TrainUtils.submitTicketTotalNum(jsonTicketInfo)
            results = []
            for i in range(totalTicketNum):
                table.add_row([i + 1,
                               TrainUtils.submitTrainInfo(i, jsonTicketInfo),
                               TrainUtils.submitCoachInfo(i, jsonTicketInfo),
                               TrainUtils.submitPassengerInfo(i, jsonTicketInfo),
                               TrainUtils.submitTicketCostInfo(i, jsonTicketInfo),
                               TrainUtils.submitTicketPayInfo(i, jsonTicketInfo),
                               ])
                results.append([i + 1,
                               TrainUtils.submitTrainInfo(i, jsonTicketInfo),
                               TrainUtils.submitCoachInfo(i, jsonTicketInfo),
                               TrainUtils.submitPassengerInfo(i, jsonTicketInfo),
                               TrainUtils.submitTicketCostInfo(i, jsonTicketInfo),
                               TrainUtils.submitTicketPayInfo(i, jsonTicketInfo),
                               ])
                if not i == totalTicketNum - 1:
                    table.add_row([2 * '-', 2 * '-', 2 * '-', 2 * '-', 2 * '-', 2 * '-'])

            print(table)

            Log.v('总张数:%d\t待支付金额:%s' % (
                totalTicketNum, Fore.YELLOW + '{}元'.format(TrainUtils.submitTicketTotalCost(jsonTicketInfo)) + Fore.RESET))
        except BaseException as e:
            return False,None
        return True,results

    def showSubmitInfo(self):
        return self._queryMyOrderNoComplete()

    def __waitForOrderId(self):
        Log.v('正在排队获取订单!')
        count = 0
        while True:
            try:
                count += 1
                status, msg, waitTime, orderId, errorMsg = self._queryOrderWaitTime()
                if not Utils.check(status, 'queryOrderWaitTime: %s' % msg):
                    return None
                Log.v('[%d]正在等待订单提交结果...' % count)
                if waitTime < 0:
                    if orderId:
                        Log.v('订单提交成功，订单号: %s' % orderId)
                        return orderId
                    elif errorMsg:
                        Log.e(errorMsg)
                        time.sleep(3)
                        return False
                    else:
                        time.sleep(3)
                        continue
                interval = waitTime // 60
                Log.w('未出票，订单排队中...预估等待时间: %s 分钟' % (interval if interval <= 30 else '超过30'))
                if interval > 30:
                    time.sleep(60)
                elif interval > 20:
                    time.sleep(30)
                elif interval > 10:
                    time.sleep(10)
                else:
                    time.sleep(3)
            except Exception as e:
                time.sleep(3)
                continue

