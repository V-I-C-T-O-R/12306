import random

import re
#此方法摘自https://github.com/testerSunshine/12306,可惜调不通,登录302
from net.NetUtils import EasyHttp


def request_alg_id(urlInfo):
    response = EasyHttp.send(urlInfo)
    # response = EasyHttp.get("https://kyfw.12306.cn/otn/HttpZF/GetJS",10)
    result = re.search(r'algID\\x3d(.*?)\\x26', response)
    try:
        return result.group(1)
    except (IndexError, AttributeError) as e:
        pass
    return ""

def get_hash_code_params():
    from collections import OrderedDict
    data = {
        'adblock': '1',
        'browserLanguage': 'en-US',
        'cookieEnabled': '1',
        'custID': '133',
        'doNotTrack': 'unknown',
        'flashVersion': '0',
        'javaEnabled': '0',
        # change
        'jsFonts': '382b3eb7cfc5d30f1b59cb283d1acaf3',
        # change
        'localCode': '3232235885',
        'mimeTypes': '52d67b2a5aa5e031084733d5006cc664',
        'os': 'MacIntel',
        'platform': 'WEB',
        'plugins': 'd22ca0b81584fbea62237b14bd04c866',
        'scrAvailSize': str(random.randint(500, 1000)) + 'x1920',
        'srcScreenSize': '24xx1080x1920',
        'storeDb': 'i1l1o1s1',
        'timeZone': '-8',
        'touchSupport': '99115dfb07133750ba677d055874de87',
        'userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.' + str(
            random.randint(
                5000, 7000)) + '.0 Safari/537.36',
        #change
        'webSmartID': '7484b4d443309cac29a8c080495fc1c0',
    }
    data_trans = {
         'os': "hAqN",
        'hasLiedResolution': "3neK",
        'userLanguage': "hLzX",
        'browserName': "-UVA",
        'localCode': "lEnu",
        'scrHeight': "5Jwy",
        'browserLanguage': "q4f3",
        'jsFonts': "EOQP",
        'localStorage': "XM7l",
        'historyList': "kU5z",
        'scrAvailWidth': "E-lJ",
        'webSmartID': "E3gR",
        'browserVersion': "d435",
        'scrDeviceXDPI': "3jCe",
        'adblock': "FMQw",
        'touchSupport': "wNLf",
        'online': "9vyE",
        'doNotTrack': "VEek",
        'timeZone': "q5aJ",
        'cookieEnabled': "VPIf",
        'plugins': "ks0Q",
        'srcScreenSize': "tOHY",
        'cookieCode': "VySQ",
        'scrAvailSize': "TeRS",
        'appMinorVersion': "qBVW",
        'cpuClass': "Md7A",
        'flashVersion': "dzuS",
        'indexedDb': "3sw-",
        'appcodeName': "qT7b",
        'openDatabase': "V8vl",
        'javaEnabled': "yD16",
        'storeDb': "Fvje",
        'scrColorDepth': "qmyu",
        'scrAvailHeight': "88tV",
        'hasLiedLanguages': "j5po",
        'mimeTypes': "jp76",
        'userAgent': "0aew",
        'sessionStorage': "HVia",
        'hasLiedOs': "ci5c",
        'systemLanguage': "e6OK",
        'scrWidth': "ssI5",
        'hasLiedBrowser': "2xC5"
    }
    data = OrderedDict(data)
    d = ''
    params = {}
    for key, item in data.items():
        d += key + item
        key = data_trans[key] if key in data_trans else key
        params[key] = item
    d_len = len(d)
    d_f = int(d_len / 3) if d_len % 3 == 0 else int(d_len / 3) + 1
    if d_len >= 3:
        d = d[d_f:2 * d_f] + d[2 * d_f:d_len] + d[0: d_f]
    d_len = len(d)
    d_f = int(d_len / 3) if d_len % 3 == 0 else int(d_len / 3) + 1
    if d_len >= 3:
        d = d[2 * d_f:d_len] + d[0: d_f] + d[1 * d_f: 2 * d_f]

    d = _encode_data_str_v2(d)
    d = _encode_data_str_v2(d)
    d = _encode_data_str_v2(d)
    data_str = _encode_string(d)
    params['hashCode'] = data_str
    return params


def _encode_data_str_v2(d):
    b = len(d)
    if b % 2 == 0:
        return d[b // 2: b] + d[0:b // 2]
    else:
        return d[b // 2 + 1:b] + d[b // 2] + d[0:b // 2]


def _encode_string(str):
    import hashlib
    import base64
    result = base64.b64encode(hashlib.sha256(str.encode()).digest()).decode()
    return result.replace('+', '-').replace('/', '_').replace('=', '')