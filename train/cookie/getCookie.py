import random
import os
from selenium import webdriver
from net import ips

def get12306Cookie():
    proxy = random.choice(ips)
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("'--proxy-server={}".format(proxy))
    browser = webdriver.Chrome(chrome_options = chromeOptions, executable_path=os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/cookie/chromedriver')
    browser.get("https://www.12306.cn/index/")
    cookies = browser.get_cookies()
    res = {}
    for cookie in cookies:
        if cookie['name'] == 'RAIL_DEVICEID':
            res['RAIL_DEVICEID'] = cookie['value']
        elif cookie['name'] == 'RAIL_EXPIRATION':
            res['RAIL_EXPIRATION'] = cookie['value']
    browser.quit()
    return res

if __name__ == '__main__':
    cookies = get12306Cookie()
    print(cookies)