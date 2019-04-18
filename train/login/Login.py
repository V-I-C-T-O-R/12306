import copy
import json
import time
from collections import OrderedDict

from conf.constant import TYPE_LOGIN_NORMAL_WAY, TYPE_LOGIN_OTHER_WAY
from conf.urls_conf import loginUrls
from configure import USER_PWD, USER_NAME
from net.NetUtils import EasyHttp
from train.login.Capthca import Captcha
from utils import Utils
from utils.Log import Log
from conf.constant import CAPTCHA_CHECK_METHOD_HAND,CAPTCHA_CHECK_METHOD_THREE,CAPTCHA_CHECK_METHOD_MYSELF

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
        # 登录有两种api
        for count in range(2):
            result, msg = self._login(userName, userPwd, autoCheck, type=(count % 2))
            if Utils.check(result, msg):
                return result, msg
        return False, '登录失败'

    @loginLogic
    def _login(self, userName, userPwd, autoCheck=2, type=TYPE_LOGIN_NORMAL_WAY):
        if type == TYPE_LOGIN_OTHER_WAY:
            self._urlInfo = loginUrls['other']
            return self._loginAsyncSuggest(userName, userPwd,autoCheck)
        self._urlInfo = loginUrls['normal']
        return self._loginNormal(userName, userPwd,autoCheck)

    def _loginNormal(self, userName, userPwd, autoCheck=2):
        status,msg = self._login_init()
        if not status:
            return status, msg
        self._uamtk_static()
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

        jsonRet = EasyHttp.send(self._urlInfo['login'], data=payload)

        def isLoginSuccess(responseJson):
            return 0 == responseJson['result_code'] if responseJson and 'result_code' in responseJson else False, \
                   responseJson[
                       'result_message'] if responseJson and 'result_message' in responseJson else '登录失败'

        result, msg = isLoginSuccess(jsonRet)
        if not result:
            return False, msg
        self._userLogin()
        self._passportRedirect()
        result, msg, apptk = self._uamtk()
        if not Utils.check(result, msg):
            return False, 'uamtk failed'
        return self._uamauthclient(apptk)

    def _loginAsyncSuggest(self, userName, userPwd, autoCheck=2):
        self._init()
        if autoCheck == CAPTCHA_CHECK_METHOD_THREE:
            results, verify = Captcha().verifyCodeAuto()
        elif autoCheck == CAPTCHA_CHECK_METHOD_HAND:
            results, verify = Captcha().verifyCaptchaByHand()
        else:
            results, verify = Captcha().verifyCodeAutoByMyself()
        if not verify:
            return False, '验证码识别错误!'
        Log.v('验证码识别成功')
        formData = OrderedDict()
        formData['loginUserDTO.user_name'] = userName
        formData['userDTO.password'] = userPwd
        formData['randCode'] = results

        jsonRet = EasyHttp.send(self._urlInfo['login'], data=formData)
        # print('loginAsyncSuggest: %s' % jsonRet)

        def isSuccess(response):
            return response['status'] and response['data'].get('loginCheck') == 'Y' if 'data' in response else False, \
                   response['data'].get('otherMsg') if 'data' in response else response['messages']

        loginSuccess, otherMsg = isSuccess(jsonRet)
        return loginSuccess, '%s:%s' % (userName, '登录成功' if loginSuccess else '登录失败')

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
        EasyHttp.send(self._urlInfo['loginInit'])
        devices_id_rsp = EasyHttp.get_custom(self._urlInfo["getDevicesId"])
        if devices_id_rsp:
            callback = devices_id_rsp.text.replace("callbackFunction('", '').replace("')", '')
            text = json.loads(callback)
            devices_id = text.get('dfp')
            exp = text.get('exp')
            EasyHttp.setCookies(RAIL_DEVICEID=devices_id,RAIL_EXPIRATION=exp)
            # Log.d('设备Id：%s'%devices_id)
            return True,'获取设备指纹成功'
        return False,'获取设备指纹失败'


if __name__ == '__main__':
    # login = Login()
    # login.login(USER_NAME, USER_PWD)
    # time.sleep(3)
    # print(login.loginOut())
    from conf.urls_conf import loginUrls
    devicesIdUrl = copy.deepcopy(loginUrls['normal']["getDevicesId"])
    devices_id_rsp = EasyHttp.get_custom(devicesIdUrl)
    print(devices_id_rsp.text)
    text = devices_id_rsp.text.replace("callbackFunction('",'').replace("')",'')
    print(text)
    j = json.loads(text)
    print(j['exp'])
    pass
