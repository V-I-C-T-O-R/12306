import os
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
    def verifyCodeAuto(self,type=TYPE_LOGIN_NORMAL_WAY):
        try:
            response = EasyHttp.send(autoVerifyUrls['12305'])

            if response['result_code'] != '0':
                return None, False
            img_base64 = response['image']

            body = {'base64': img_base64}
            response = requests.post(autoVerifyUrls['api']['url'],json=body,headers ={
                'Content-Type': 'application/json',
            }).json()

            if response['success'] != True:
                return None, False
            body = {
                'check': response['data']['check'],
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

    def verifyCodeAutoByMyself(self,type=TYPE_LOGIN_NORMAL_WAY):
        try:
            urlInfo = loginUrls['other']['captcha'] if type == TYPE_LOGIN_OTHER_WAY else loginUrls['normal']['captcha']
            Log.v('正在获取验证码..')

            response = EasyHttp.send(urlInfo)
            address = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/image_captcha/'

            byte_stream = BytesIO(response)
            roiImg = Image.open(byte_stream)  # Image打开二进制流Byte字节流数据
            imgByteArr = BytesIO()  # 创建一个空的Bytes对象
            roiImg.save(imgByteArr, format='PNG')  # PNG就是图片格式，我试过换成JPG/jpg都不行
            imgByteArr = imgByteArr.getvalue()  # 这个就是保存的二进制流
            file_name = '1.jpg'
            file_path = address + file_name
            # 下面这一步只是本地测试， 可以直接把imgByteArr，当成参数上传到七牛云
            with open(file_path, "wb") as f:
                f.write(imgByteArr)

            from train.image_captcha import cut_image
            results = cut_image.cut_image(address,file_name)
            results = self.__indexTransCaptchaResults(results)

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
    # Captcha().VerifyCodeAuto()
    # print(Captcha().VerifyCodeAutoByMyself())
    body = \
        {
            "base64": "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"
        }
    # response = EasyHttp.send(autoVerifyUrls['api'], json=body)

    response = requests.post('https://12306.jiedanba.cn/api/v2/getCheck',json=body,headers ={
                'Content-Type': 'application/json',
            })
    print(response.content)
    pass
