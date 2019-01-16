import time

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
        for count in range(10):
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
            return response['result_code'] == 0 if 'result_code' in response else False

        return isSuccess(jsonRet), \
               jsonRet['result_message'] if 'result_message' in jsonRet else 'no result_message', \
               jsonRet['newapptk'] if 'newapptk' in jsonRet else 'no newapptk'

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
        self._init()
        self._uamtk()
        if autoCheck == CAPTCHA_CHECK_METHOD_THREE:
            if not Captcha().verifyCodeAuto()[1]:
                return False, '验证码识别错误!'
        elif autoCheck == CAPTCHA_CHECK_METHOD_HAND:
            if not Captcha().verifyCaptchaByHand()[1]:
                return False, '验证码识别错误!'
        else:
            if not Captcha().verifyCodeAutoByMyself()[1]:
                return False, '验证码识别错误!'
        payload = {
            'username': userName,
            'password': userPwd,
            'appid': 'otn',
        }
        jsonRet = EasyHttp.send(self._urlInfo['login'], data=payload)

        def isLoginSuccess(responseJson):
            return 0 == responseJson['result_code'] if responseJson and 'result_code' in responseJson else False, \
                   responseJson[
                       'result_message'] if responseJson and 'result_message' in responseJson else 'login failed'

        result, msg = isLoginSuccess(jsonRet)
        if not result:
            return False, msg
        # self._userLogin()
        self._passportRedirect()
        result, msg, apptk = self._uamtk()
        if not Utils.check(result, msg):
            return False, 'uamtk failed'
        return self._uamauthclient(apptk)

    def _loginAsyncSuggest(self, userName, userPwd, autoCheck=2):
        self._init()
        if autoCheck == CAPTCHA_CHECK_METHOD_THREE:
            results, verify = Captcha().verifyCodeAuto(type=TYPE_LOGIN_OTHER_WAY)
        elif autoCheck == CAPTCHA_CHECK_METHOD_HAND:
            results, verify = Captcha().verifyCaptchaByHand(type=TYPE_LOGIN_OTHER_WAY)
        else:
            results, verify = Captcha().verifyCodeAutoByMyself(type=TYPE_LOGIN_OTHER_WAY)
        if not verify:
            return False, '验证码识别错误!'
        formData = {
            'loginUserDTO.user_name': userName,
            'userDTO.password': userPwd,
            'randCode': results,
        }
        jsonRet = EasyHttp.send(self._urlInfo['login'], data=formData)
        # print('loginAsyncSuggest: %s' % jsonRet)

        def isSuccess(response):
            return response['status'] and response['data']['loginCheck'] == 'Y' if 'data' in response else False, \
                   response['data']['otherMsg'] if 'data' in response else response['messages']

        loginSuccess, otherMsg = isSuccess(jsonRet)
        return loginSuccess, '%s:%s' % (userName, otherMsg or '登录成功!')

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


if __name__ == '__main__':
    login = Login()
    login.login(USER_NAME, USER_PWD)
    time.sleep(3)
    print(login.loginOut())
