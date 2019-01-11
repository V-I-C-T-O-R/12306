import collections
import random
import time

import requests

from conf.urls_conf import queryUrls
from define.UserAgent import USER_AGENT


def sendLogic(func):
    def wrapper(*args, **kw):
        for count in range(10):
            response = func(*args, **kw)
            if response:
                return response
            else:
                time.sleep(0.1)
        return None

    return wrapper


class EasyHttp(object):
    __session = requests.Session()

    @staticmethod
    def updateHeaders(headers):
        EasyHttp.__session.headers.update(headers)

    @staticmethod
    def resetHeaders():
        EasyHttp.__session.headers.clear()
        EasyHttp.__session.headers.update({
            'Host': r'kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/login/init',
            'User-Agent': random.choice(USER_AGENT),
            "Accept-Encoding": "gzip, deflate, br",
            "X-Requested-With": "XMLHttpRequest"
        })

    @staticmethod
    def setCookies(**kwargs):
        for k, v in kwargs.items():
            EasyHttp.__session.cookies.set(k, v)

    @staticmethod
    def removeCookies(key=None):
        EasyHttp.__session.cookies.set(key, None) if key else EasyHttp.__session.cookies.clear()

    @staticmethod
    @sendLogic
    def send(urlInfo, params=None, data=None, **kwargs):
        EasyHttp.resetHeaders()
        if 'headers' in urlInfo and urlInfo['headers']:
            EasyHttp.updateHeaders(urlInfo['headers'])
        try:
            response = EasyHttp.__session.request(method=urlInfo['method'],
                                                  url=urlInfo['url'],
                                                  params=params,
                                                  data=data,
                                                  timeout=10,
                                                  allow_redirects=False,
                                                  **kwargs)
            if response.status_code == requests.codes.ok:
                if 'response' in urlInfo:
                    if urlInfo['response'] == 'binary':
                        return response.content
                    if urlInfo['response'] == 'html':
                        response.encoding = response.apparent_encoding
                        return response.text
                return response.json()
        except:
            pass
        return None


if __name__ == '__main__':
    dic = collections.OrderedDict()
    dic['leftTicketDTO.train_date'] = '2019-01-01'
    dic['leftTicketDTO.from_station'] = 'SHH'
    dic['leftTicketDTO.to_station'] = 'GZQ'
    dic['purpose_codes'] = 'ADULT'
    # params = {
    #     r'leftTicketDTO.train_date': '2019-01-01',
    #     r'leftTicketDTO.from_station': 'SHH',
    #     r'leftTicketDTO.to_station': 'GZQ',
    #     r'purpose_codes': "ADULT"
    # }

    headers = {"X-Requested-With": "XMLHttpRequest",
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36",
               "Accept-Encoding": "gzip, deflate, br",
               "Content-Type": "application/json;charset=utf-8"}
    url = queryUrls['query']['url'] + "?leftTicketDTO.train_date=" + '2019-01-01' + "&leftTicketDTO.from_station=" + 'SHH' + "&leftTicketDTO.to_station=" + 'GZQ' + "&purpose_codes=ADULT"
    result = requests.get(url,headers=headers,  timeout=15)
    print("---------------------------------------------------------------------")
    print(result.content)
    print("---------------------------------------------------------------------")
    print(EasyHttp.send(queryUrls['query'],params=dic))
    pass
