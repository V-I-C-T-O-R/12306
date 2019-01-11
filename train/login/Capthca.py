import random
from io import BytesIO

import requests
from PIL import Image

from conf.constant import TYPE_LOGIN_NORMAL_WAY, TYPE_LOGIN_OTHER_WAY
from conf.urls_conf import loginUrls, autoVerifyUrls
from net.NetUtils import EasyHttp
from train.login import damatuWeb
from utils import FileUtils
from utils.Log import Log


class Captcha(object):
    __REPONSE_NORMAL_CDOE_SUCCESSFUL = '4'
    __REPONSE_OHTER_CDOE_SUCCESSFUL = '1'
    __CAPTCHA_PATH = 'captcha.jpg'

    def getCaptcha(self, type=TYPE_LOGIN_NORMAL_WAY):
        urlInfo = loginUrls['other']['captcha'] if type == TYPE_LOGIN_OTHER_WAY else loginUrls['normal']['captcha']
        Log.v('正在获取验证码..')
        return EasyHttp.send(urlInfo)

    def check(self, results, type=TYPE_LOGIN_NORMAL_WAY):
        if type == TYPE_LOGIN_OTHER_WAY:
            return self._checkRandCodeAnsyn(results)
        return self._captchaCheck(results)

    def _checkRandCodeAnsyn(self, results):
        formData = {
            'randCode': results,
            'rand': 'sjrand',
        }
        jsonRet = EasyHttp.send(loginUrls['other']['captchaCheck'], data=formData)
        print('checkRandCodeAnsyn: %s' % jsonRet)

        def verify(response):
            return response['status'] and Captcha.__REPONSE_OHTER_CDOE_SUCCESSFUL == response['data']['result']

        return verify(jsonRet)

    def _captchaCheck(self, results):
        data = {
            'answer': results,
            'login_site': 'E',
            'rand': 'sjrand',
        }
        jsonRet = EasyHttp.send(loginUrls['normal']['captchaCheck'], data=data)
        # print('captchaCheck: %s' % jsonRet)

        def verify(response):
            return Captcha.__REPONSE_NORMAL_CDOE_SUCCESSFUL == response[
                'result_code'] if 'result_code' in response else False

        return verify(jsonRet)

    def verifyCaptchaByClound(self, type=TYPE_LOGIN_NORMAL_WAY):
        captchaContent = self.getCaptcha(type)
        if captchaContent:
            FileUtils.saveBinary(Captcha.__CAPTCHA_PATH, captchaContent)
        else:
            Log.e('failed to save captcha')
            return None
        results = damatuWeb.verify(Captcha.__CAPTCHA_PATH)
        results = self.__cloundTransCaptchaResults(results)
        Log.v('captchaResult: %s' % results)
        return results, self.check(results)

    # 通过人眼手动识别12306验证码
    def verifyCaptchaByHand(self, type=TYPE_LOGIN_NORMAL_WAY):
        img = None
        try:
            img = Image.open(BytesIO(self.getCaptcha(type)))
            img.show()
            Log.v(
                """ 
                -----------------
                | 0 | 1 | 2 | 3 |
                -----------------
                | 4 | 5 | 6 | 7 |
                ----------------- """)
            results = input("输入验证码索引(见上图，以','分割）: ")
        except BaseException as e:
            return None, False
        finally:
            if img is not None:
                img.close()
        results = self.__indexTransCaptchaResults(results)
        Log.v('captchaResult: %s' % results)
        return results, self.check(results, type)

    def __indexTransCaptchaResults(self, indexes, sep=r','):
        coordinates = ['40,40', '110,40', '180,40', '250,40', '40,110', '110,110', '180,110', '250,110']
        results = []
        for index in indexes.split(sep=sep):
            results.append(coordinates[int(index)])
        return ','.join(results)

    def __cloundTransCaptchaResults(self, results):
        if type(results) != str:
            return ''
        offsetY = 30
        results = results.replace(r'|', r',').split(r',')
        for index in range(0, len(results)):
            if index % 2 != 0:
                results[index] = str(int(results[index]) - offsetY)
        return ','.join(results)

    # 通过第三方接口自动识别12306验证码
    def VerifyCodeAuto(self,type=TYPE_LOGIN_NORMAL_WAY):
        url_12305 = 'https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand&'.format(
            random.random())
        try:
            response = EasyHttp.send(autoVerifyUrls['12305'])

            if response['result_code'] != '0':
                return None, False
            img_base64 = response['image']

            body = {'base64': img_base64}
            response = EasyHttp.send(autoVerifyUrls['api'],json=body)

            if response['success'] != True:
                return None, False
            body = {
                'check': response['check'],
                'img_buf': img_base64,
                'logon': 1,
                'type': 'D'}
            response = requests.post(autoVerifyUrls['img_url']['url'],json=body).json()
            content = str(response['res'])
            results = content.replace('(','').replace(')','')

        except Exception as e:
            Log.w(e)
            return None, False
        return results, self._captchaAutoCheck(results)

    #对应自动验证验证码操作
    def _captchaAutoCheck(self, results):

        params = {
            'answer': results,
            'login_site': 'E',
            'rand': 'sjrand',
        }
        jsonRet = EasyHttp.send(autoVerifyUrls['check_url'],params=params)

        # print('captchaCheck: %s' % jsonRet)

        def verify(response):
            return Captcha.__REPONSE_NORMAL_CDOE_SUCCESSFUL == response[
                'result_code'] if 'result_code' in response else False

        return verify(jsonRet)

if __name__ == '__main__':
    Captcha().VerifyCodeAuto()
    pass
