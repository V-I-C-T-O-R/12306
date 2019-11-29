import random
import os
import time
from selenium import webdriver
from net import ips

def get12306Cookie():
    proxy = random.choice(ips)
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("'--proxy-server={}".format(proxy))
    browser = webdriver.Chrome(chrome_options=chromeOptions, executable_path=os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))) + '/cookie/chromedriver')
    browser.get("https://www.12306.cn/index/")
    flag = False
    res = {}
    while (flag == False):
        cookies = browser.get_cookies()
        for cookie in cookies:
            if cookie['name'] == 'RAIL_DEVICEID':
                res['RAIL_DEVICEID'] = cookie['value']
                flag = True
            elif cookie['name'] == 'RAIL_EXPIRATION':
                res['RAIL_EXPIRATION'] = cookie['value']
        time.sleep(1)
    browser.quit()
    return res


if __name__ == '__main__':
    cookies = get12306Cookie()
    print(cookies)
