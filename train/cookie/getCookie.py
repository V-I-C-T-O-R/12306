import random
import os
import time
from selenium import webdriver
from net import ips
import platform
from utils.Log import Log

def get12306Cookie():
    proxy = random.choice(ips)
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("'--proxy-server={}".format(proxy))
    chromeOptions.add_argument('--headless')  # 浏览器不提供可视化页面
    browser = webdriver.Chrome(chrome_options=chromeOptions, executable_path=get_platform_driver())
    try:
        browser.get("https://www.12306.cn/index/")
        res = {}
        count = 0
        max_count = 100
        while(1):
            count += 1
            Log.v('正在第{}次请求设备指纹...'.format(count))
            time.sleep(0.2)
            cookies = browser.get_cookies()
            for cookie in cookies:
                res[cookie["name"]] = cookie["value"]

            if res.get('RAIL_DEVICEID') and res.get('RAIL_EXPIRATION'):
                break
            #强制退出等待
            if count >= max_count:
                return False, '获取设备请求达到最大次数{},请查看当前是否已被12306加入小黑屋'.format(max_count)
    except Exception as e:
        return False,'网络尝试获取设备指纹请求失败'
    finally:
        browser.quit()
    Log.v('请求设备指纹成功')
    return True,res

def get_platform_driver():
    sysstr = platform.system()
    root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/cookie/'
    if (sysstr == "Windows"):
        return root_path + 'chromedriver.exe'
    elif (sysstr == "Linux"):
        return root_path + 'chromedriver-linux'
    else:
        #暂时默认除了linux和windows就是mac
        return root_path + 'chromedriver-mac'

if __name__ == '__main__':
    # cookies = get12306Cookie()
    # print(cookies)
    print(platform.system())
