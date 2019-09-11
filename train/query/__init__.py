from conf.urls_conf import loginUrls
from net.NetUtils import EasyHttp
from utils.Log import Log


def check_re_login():
    response = EasyHttp.post_custom(loginUrls['normal']['conf'])
    if not response or not response.json():
        return False
    resp = response.json()
    login_status = resp.get('data').get('is_login')
    Log.d('登录状态：%s' % login_status)
    if 'Y' != login_status:
        Log.d('登录状态已过期,重新请求')
        return False
    return True