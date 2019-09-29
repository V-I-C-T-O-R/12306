from conf.urls_conf import loginUrls
from net.NetUtils import EasyHttp
from utils.Log import Log

def check_login_magic(func):
    def wrapper(*args, **kw):
        reslut = False
        msg = ''
        for count in range(4):
            reslut, msg = func(*args, **kw)
            if reslut:
                break
            #目测12306拉取状态最少3次,最多次数暂定为4
            if count > 2:
                Log.d(msg)
        return reslut, msg

    return wrapper

@check_login_magic
def check_re_login():
    try:
        response = EasyHttp.post_custom(loginUrls['normal']['conf'])
        if not response or not response.json():
            return False
        resp = response.json()
        login_status = resp.get('data').get('is_login')
        # Log.d('登录状态：%s' % login_status)
        if 'Y' != login_status:
            # Log.d('登录状态已过期')
            return False,'登录状态已过期'
    except Exception as e:
        return False,'查询登录返回状态异常'
    return True,'ok'