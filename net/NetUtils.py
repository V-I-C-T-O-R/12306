import collections
import random
import time
from http import cookiejar

from lxml import html

import requests

from conf.urls_conf import queryUrls
from define.UserAgent import USER_AGENT
from net import ips

def sendLogic(func):
    def wrapper(*args, **kw):
        for count in range(5):
            response = func(*args, **kw)
            if response is not None:
                return response
            else:
                time.sleep(0.1)
        return None

    return wrapper


class EasyHttp(object):
    __session = requests.Session()

    @staticmethod
    def get_session():
        return EasyHttp.__session

    @staticmethod
    def load_cookies(cookie_path):
        load_cookiejar = cookiejar.LWPCookieJar()
        load_cookiejar.load(cookie_path, ignore_discard=True, ignore_expires=True)
        load_cookies = requests.utils.dict_from_cookiejar(load_cookiejar)
        EasyHttp.__session.cookies = requests.utils.cookiejar_from_dict(load_cookies)

    @staticmethod
    def save_cookies(cookie_path):
        new_cookie_jar = cookiejar.LWPCookieJar(cookie_path)
        requests.utils.cookiejar_from_dict({c.name: c.value for c in EasyHttp.__session.cookies}, new_cookie_jar)
        new_cookie_jar.save(cookie_path, ignore_discard=True, ignore_expires=True)

    @staticmethod
    def updateHeaders(headers):
        EasyHttp.__session.headers.update(headers)

    @staticmethod
    def resetHeaders():
        EasyHttp.__session.headers.clear()
        EasyHttp.__session.headers.update({
            'User-Agent': random.choice(USER_AGENT),
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
            if len(ips) == 0:
                response = EasyHttp.__session.request(method=urlInfo['method'],
                                                      url=urlInfo['url'],
                                                      params=params,
                                                      data=data,
                                                      timeout=3,
                                                      allow_redirects=False,
                                                      **kwargs)
            else:
                proxy_address = random.choice(ips)
                response = EasyHttp.__session.request(method=urlInfo['method'],
                                                      url=urlInfo['url'],
                                                      params=params,
                                                      data=data,
                                                      #python3发现proxies写成{"https": "https://{}"}的形式没法访问,笑哭-_-
                                                      proxies={"http": "http://{}".format(proxy_address[0])},
                                                      timeout=3,
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
            if ips:
                ips.remove(proxy_address)
        return None

    @staticmethod
    @sendLogic
    def getHtmlTree(url, **kwargs):
        """
        获取html树
        """
        time.sleep(1)
        headers = {'Connection': 'keep-alive',
                  'Cache-Control': 'max-age=0',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Accept-Encoding': 'gzip, deflate, sdch',
                  'Accept-Language': 'zh-CN,zh;q=0.8',
                  }
        try:
            response = EasyHttp.__session.request(method='GET',
                                       url=url,
                                       # headers=headers,
                                       timeout=3,
                                       allow_redirects=False,
                                       **kwargs)
            if response.status_code == requests.codes.ok:
                return html.etree.HTML(response.text)
        except Exception as e:
            return None
        return None

    @staticmethod
    @sendLogic
    def get(url,timeout):
        try:
            response = EasyHttp.__session.request(method='GET',
                                                  url=url,
                                                  timeout=timeout,
                                                  allow_redirects=False)
            if response.status_code == requests.codes.ok:
                return response.text
        except Exception as e:
            return None
        return None

    @staticmethod
    @sendLogic
    def get_custom(urlInfo):
        try:
            response = EasyHttp.__session.request(method=urlInfo['method'],
                                                      url=urlInfo['url'],
                                                      timeout=3,
                                                      allow_redirects=False
                                                    )
        except Exception as e:
            return None
        return response

    @staticmethod
    @sendLogic
    def post_custom(urlInfo,data=None):
        EasyHttp.resetHeaders()
        if 'headers' in urlInfo and urlInfo['headers']:
            EasyHttp.updateHeaders(urlInfo['headers'])
        try:
            if len(ips) == 0:
                response = EasyHttp.__session.request(method=urlInfo['method'],
                                                      url=urlInfo['url'],
                                                      data=data,
                                                      timeout=3,
                                                      allow_redirects=False)
            else:
                proxy_address = random.choice(ips)
                response = EasyHttp.__session.request(method=urlInfo['method'],
                                                      url=urlInfo['url'],
                                                      data=data,
                                                      proxies={"http": "http://{}".format(proxy_address[0])},
                                                      timeout=3,
                                                      allow_redirects=False)
        except Exception as e:
            if ips:
                ips.remove(proxy_address)
            return None
        return response

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
