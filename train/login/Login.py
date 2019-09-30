import copy
import json
import time
from collections import OrderedDict

import requests

from conf.urls_conf import loginUrls
from conf.constant import CAPTCHA_CHECK_METHOD_HAND, CAPTCHA_CHECK_METHOD_THREE
from net.NetUtils import EasyHttp
from train.login.Capthca import Captcha
from utils import Utils
from utils.Log import Log

def loginLogic(func):
    def wrapper(*args, **kw):
        reslut = False
        msg = ''
        for count in range(20):
            Log.v('第%s次尝试获取验证图片' % str(count + 1))
            reslut, msg = func(*args, **kw)
            if reslut:
                break
            Log.w(msg)
        return reslut, msg

    return wrapper


class Login(object):
    __LOGIN_SUCCESS_RESULT_CODE = 0

    def _passportRedirect(self):
        params = {
            'redirect': '/otn/login/userLogin',
        }
        EasyHttp.send(self._urlInfo['userLoginRedirect'])

    def _userLogin(self):
        params = {
            '_json_att': '',
        }
        EasyHttp.send(self._urlInfo['userLogin'])

    def _uamtk(self):
        jsonRet = EasyHttp.send(self._urlInfo['uamtk'], data={'appid': 'otn'})

        def isSuccess(response):
            return response['result_code'] == 0 if response and 'result_code' in response else False

        return isSuccess(jsonRet), \
               jsonRet['result_message'] if jsonRet and 'result_message' in jsonRet else 'no result_message', \
               jsonRet['newapptk'] if jsonRet and 'newapptk' in jsonRet else 'no newapptk'

    def _uamtk_static(self):
        EasyHttp.send(self._urlInfo['conf'])
        jsonRet = EasyHttp.send(self._urlInfo['uamtk-static'], data={'appid': 'otn'})

        def isSuccess(response):
            return response['result_code'] == 0 if response and 'result_code' in response else False

        return isSuccess(jsonRet), \
               jsonRet['result_message'] if jsonRet and 'result_message' in jsonRet else 'no result_message', \
               jsonRet['newapptk'] if jsonRet and 'newapptk' in jsonRet else 'no newapptk'

    def _uamauthclient(self, apptk):
        jsonRet = EasyHttp.send(self._urlInfo['uamauthclient'], data={'tk': apptk})

        # print(jsonRet)

        def isSuccess(response):
            return response['result_code'] == 0 if response and 'result_code' in response else False

        return isSuccess(jsonRet), '%s:%s' % (jsonRet['username'], jsonRet['result_message']) if jsonRet \
            else 'uamauthclient failed'

    def login(self, userName, userPwd, autoCheck=2):
        self._urlInfo = loginUrls['normal']
        status, msg = self._login_init()
        if not status:
            return status, msg
        self._uamtk_static()

        result, msg = self._login(userName, userPwd, autoCheck)
        if Utils.check(result, msg):
            return result, msg
        return False, '登录失败'

    @loginLogic
    def _login(self, userName, userPwd, autoCheck=2):
        return self._loginNormal(userName, userPwd,autoCheck)

    def _loginNormal(self, userName, userPwd, autoCheck=2):
        if autoCheck == CAPTCHA_CHECK_METHOD_THREE:
            results, verify = Captcha().verifyCodeAuto()
        elif autoCheck == CAPTCHA_CHECK_METHOD_HAND:
            results, verify = Captcha().verifyCaptchaByHand()
        else:
            results, verify = Captcha().verifyCodeAutoByMyself()

        if not verify:
            return False, '验证码识别错误!'
        Log.v('验证码识别成功')
        payload = OrderedDict()
        payload['username'] = userName
        payload['password'] = userPwd
        payload['appid'] = 'otn'
        payload['answer'] = results

        response = EasyHttp.post_custom(self._urlInfo['login'], data=payload)

        def isLoginSuccess(responseJson):
            return 0 == responseJson['result_code'] if responseJson and 'result_code' in responseJson else False, \
                   responseJson[
                       'result_message'] if responseJson and 'result_message' in responseJson else '登录失败'

        if response.status_code != requests.codes.ok:
            return False, "登录请求被强制重定向,准备重试..."
        result, msg = isLoginSuccess(response.json())
        if not result :
            return False, msg
        self._userLogin()
        self._passportRedirect()
        result, msg, apptk = self._uamtk()
        if not Utils.check(result, msg):
            return False, 'uamtk failed'
        return self._uamauthclient(apptk)

    def isLogin(self):
        formData = {
            '_json_att': ''
        }
        jsonRet = EasyHttp.send(self._urlInfo['checkUser'])
        Log.d('checkUser: %s' % jsonRet)
        return jsonRet['data']['flag'] if jsonRet and 'data' in jsonRet and 'flag' in jsonRet[
            'data'] else False

    def loginOut(self):
        EasyHttp.send(self._urlInfo['loginOut'])
        self._init()
        return self._uamtk()

    def _init(self):
        EasyHttp.send(self._urlInfo['init'])

    def _login_init(self):
        #死方法来手动每次更新deviceid url
        url_info = copy.deepcopy(self._urlInfo["getDevicesId"])
        url_info['url'] = self._urlInfo["getDevicesId"]['url'] + str(int(time.time()*1000))
        devices_id_rsp = EasyHttp.get_custom(url_info)

        # params = {"algID": request_alg_id(self._urlInfo['getJS']), "timestamp": int(time.time() * 1000)}
        # params = dict(params, **get_hash_code_params())
        # devices_id_rsp = EasyHttp.send(self._urlInfo["getDevicesId"],params=params)
        if devices_id_rsp:
            callback = devices_id_rsp.text[18:-2]
            # callback = devices_id_rsp.replace("callbackFunction('", '').replace("')", '')
            try:
                text = json.loads(callback)
                devices_id = text.get('dfp')
                exp = text.get('exp')
            except Exception as e:
                return False,'获取设备指纹失败'
            EasyHttp.setCookies(RAIL_DEVICEID=devices_id, RAIL_EXPIRATION=exp)
            # Log.d('设备Id：%s'%devices_id)
            return True, '获取设备指纹成功'
        EasyHttp.send(self._urlInfo['index'])
        EasyHttp.send(self._urlInfo['loginInit'])
        return False,'获取设备指纹失败'


if __name__ == '__main__':
    # login = Login()
    # login.login(USER_NAME, USER_PWD)
    # time.sleep(3)
    # print(login.loginOut())
    devicesIdUrl = copy.deepcopy(loginUrls['normal']["getDevicesId"])
    devices_id_rsp = EasyHttp.get_custom(devicesIdUrl)
    print(devices_id_rsp.text)
    text = devices_id_rsp.text.replace("callbackFunction('",'').replace("')",'')
    print(text)
    j = json.loads(text)
    print(j['exp'])
    pass
