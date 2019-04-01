import multiprocessing
import os
import re
from utils.Log import Log
import requests
import threadpool

from net.NetUtils import EasyHttp
from utils.sqllite_handle import Sqlite

requests.packages.urllib3.disable_warnings()
address = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/'
"""
    66ip.cn  无效
    data5u.com
    xicidaili.com
    goubanjia.com
    xdaili.cn
    kuaidaili.com
    cn-proxy.com
    proxy-list.org
    www.mimiip.com to do
"""


class GetFreeProxy(object):

    @staticmethod
    def freeProxySecond(area=33, page=1):
        """
        代理66 http://www.66ip.cn/
        :param area: 抓取代理页数，page=1北京代理页，page=2上海代理页......
        :param page: 翻页
        :return:
        """
        area = 33 if area > 33 else area
        for area_index in range(1, area + 1):
            for i in range(1, page + 1):
                url = "http://www.66ip.cn/areaindex_{}/{}.html".format(area_index, i)
                html_tree = EasyHttp.getHtmlTree(url)
                if html_tree is None:
                    Log.w('http://www.66ip.cn无效')
                    return []
                tr_list = html_tree.xpath("//*[@id='footer']/div/table/tr[position()>1]")
                if len(tr_list) == 0:
                    continue
                for tr in tr_list:
                    yield tr.xpath("./td[1]/text()")[0] + ":" + tr.xpath("./td[2]/text()")[0]
                break

    @staticmethod
    def freeProxyFourth(page_count=2):
        """
        西刺代理 http://www.xicidaili.com
        :return:
        """
        url_list = [
            'http://www.xicidaili.com/nn/',  # 高匿
            'http://www.xicidaili.com/nt/',  # 透明
        ]
        for each_url in url_list:
            for i in range(1, page_count + 1):
                page_url = each_url + str(i)
                tree = EasyHttp.getHtmlTree(page_url)
                if not tree:
                    Log.w('http://www.xicidaili.com无效')
                    return []
                proxy_list = tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
                for proxy in proxy_list:
                    try:
                        yield ':'.join(proxy.xpath('./td/text()')[0:2])
                    except Exception as e:
                        pass

    @staticmethod
    def freeProxyFifth():
        """
        guobanjia http://www.goubanjia.com/
        :return:
        """
        url = "http://www.goubanjia.com/"
        tree = EasyHttp.getHtmlTree(url)
        if tree is None:
            Log.w('http://www.goubanjia.com无效')
            return []
        proxy_list = tree.xpath('//td[@class="ip"]')
        # 此网站有隐藏的数字干扰，或抓取到多余的数字或.符号
        # 需要过滤掉<p style="display:none;">的内容
        xpath_str = """.//*[not(contains(@style, 'display: none'))
                                        and not(contains(@style, 'display:none'))
                                        and not(contains(@class, 'port'))
                                        ]/text()
                                """
        for each_proxy in proxy_list:
            try:
                # :符号裸放在td下，其他放在div span p中，先分割找出ip，再找port
                ip_addr = ''.join(each_proxy.xpath(xpath_str))
                port = each_proxy.xpath(".//span[contains(@class, 'port')]/text()")[0]
                yield '{}:{}'.format(ip_addr, port)
            except Exception as e:
                pass

    @staticmethod
    def freeProxySixth():
        """
        讯代理 http://www.xdaili.cn/
        :return:
        """
        url = 'http://www.xdaili.cn/ipagent/freeip/getFreeIps?page=1&rows=10'
        
        try:
            res = EasyHttp.get(url, timeout=10).json()
            if not res or not res['RESULT'] or not res['RESULT']['rows']:
                Log.w('http://www.goubanjia.com无效')
                return []
            for row in res['RESULT']['rows']:
                yield '{}:{}'.format(row['ip'], row['port'])
        except Exception as e:
            pass

    @staticmethod
    def freeProxySeventh():
        """
        快代理 https://www.kuaidaili.com
        """
        url_list = [
            'https://www.kuaidaili.com/free/inha/{page}/',
            'https://www.kuaidaili.com/free/intr/{page}/'
        ]
        for url in url_list:
            for page in range(1, 2):
                page_url = url.format(page=page)
                tree = EasyHttp.getHtmlTree(page_url)
                if tree is None:
                    Log.w('http://www.kuaidaili.com无效')
                    return []
                proxy_list = tree.xpath('.//table//tr')
                for tr in proxy_list[1:]:
                    yield ':'.join(tr.xpath('./td/text()')[0:2])

    @staticmethod
    def freeProxyEight():
        """
        秘密代理 http://www.mimiip.com
        """
        url_gngao = ['http://www.mimiip.com/gngao/%s' % n for n in range(1, 2)]  # 国内高匿
        url_gnpu = ['http://www.mimiip.com/gnpu/%s' % n for n in range(1, 2)]  # 国内普匿
        url_gntou = ['http://www.mimiip.com/gntou/%s' % n for n in range(1, 2)]  # 国内透明
        url_list = url_gngao + url_gnpu + url_gntou

        
        for url in url_list:
            r = EasyHttp.get(url, timeout=10)
            if not r:
                Log.w('http://www.mimiip.com无效')
                return []
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W].*<td>(\d+)</td>', r)
            for proxy in proxies:
                yield ':'.join(proxy)

    @staticmethod
    def freeProxyNinth():
        """
        码农代理 https://proxy.coderbusy.com/
        :return:
        """
        urls = ['https://proxy.coderbusy.com/classical/country/cn.aspx?page=1']
        
        for url in urls:
            r = EasyHttp.get(url, timeout=10)
            if not r:
                Log.w('http://proxy.coderbusy.com无效')
                return []
            proxies = re.findall('data-ip="(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})".+?>(\d+)</td>', r)
            for proxy in proxies:
                yield ':'.join(proxy)

    @staticmethod
    def freeProxyTen():
        """
        云代理 http://www.ip3366.net/free/
        :return:
        """
        urls = ['http://www.ip3366.net/free/']
        
        for url in urls:
            r = EasyHttp.get(url, timeout=10)
            if not r:
                Log.w('http://www.ip3366.com无效')
                return []
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxyEleven():
        """
        IP海 http://www.iphai.com/free/ng
        :return:
        """
        urls = [
            'http://www.iphai.com/free/ng',
            'http://www.iphai.com/free/np',
            'http://www.iphai.com/free/wg',
            'http://www.iphai.com/free/wp'
        ]
        
        for url in urls:
            r = EasyHttp.get(url, timeout=10)
            if not r:
                Log.w('http://www.iphai.com无效')
                return []
            proxies = re.findall(r'<td>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</td>[\s\S]*?<td>\s*?(\d+)\s*?</td>',
                                 r)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxyTwelve(page_count=2):
        """
        guobanjia http://ip.jiangxianli.com/?page=
        免费代理库
        超多量
        :return:
        """
        for i in range(1, page_count + 1):
            url = 'http://ip.jiangxianli.com/?page={}'.format(i)
            html_tree = EasyHttp.getHtmlTree(url)
            if html_tree is None:
                Log.w('http://ip.jiangxianli.com无效')
                return []
            tr_list = html_tree.xpath("/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr")
            if len(tr_list) == 0:
                continue
            for tr in tr_list:
                yield tr.xpath("./td[2]/text()")[0] + ":" + tr.xpath("./td[3]/text()")[0]

    @staticmethod
    def freeProxyWallFirst():
        """
        墙外网站 cn-proxy
        :return:
        """
        urls = ['http://cn-proxy.com/', 'http://cn-proxy.com/archives/218']
        
        for url in urls:
            r = EasyHttp.get(url, timeout=10)
            if not r:
                Log.w('http://cn-proxy.com无效')
                return []
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W]<td>(\d+)</td>', )
            for proxy in proxies:
                yield ':'.join(proxy)

    @staticmethod
    def freeProxyWallSecond():
        """
        https://proxy-list.org/english/index.php
        :return:
        """
        urls = ['https://proxy-list.org/english/index.php?p=%s' % n for n in range(1, 10)]
        
        import base64
        for url in urls:
            r = EasyHttp.get(url, timeout=10)
            if not r:
                Log.w('http://proxy-list.org/english/index.php无效')
                return []
            proxies = re.findall(r"Proxy\('(.*?)'\)", r)
            for proxy in proxies:
                yield base64.b64decode(proxy).decode()

    @staticmethod
    def freeProxyWallThird():
        urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1']
        
        for url in urls:
            r = EasyHttp.get(url, timeout=10)
            if not r:
                Log.w('http://list.proxylistplus.com无效')
                return []
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r)
            for proxy in proxies:
                yield ':'.join(proxy)

    def verifyProxyFormat(proxy):
        """
        检查代理格式
        :param proxy:
        :return:
        """
        import re
        verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
        _proxy = re.findall(verify_regex, proxy)
        return True if len(_proxy) == 1 and _proxy[0] == proxy else False

    @staticmethod
    def validUsefulProxy(params):
        """
        检验代理是否可用
        """
        marks = params.split('&&')
        if isinstance(marks[1], bytes):
            marks[1] = marks[1].decode('utf8')
        proxies = {"http": "http://{proxy}".format(proxy=marks[1])}
        flag = None
        try:
            # 超过20秒的代理就不要了
            r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10, verify=False)
            if r.status_code == 200 and r.json().get("origin"):
                # logger.info('%s is ok' % proxy)
                flag = True
        except Exception as e:
            flag = False
        if not flag:
            sqlite = Sqlite(address + 'ip.db')
            sqlite.update_data('delete from ip_house where id = {}'.format(marks[0]))
            Log.d("删除无效代理:" + marks[1])

    @staticmethod
    def getAllProxy(pool_size=10,thread_or_process=True,is_refash=True):

        Log.v('正在更新ip池,请稍后...')
        # address = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/'
        if is_refash:
            proxys = GetFreeProxy.get_list_proxys()
            proxys = list(set(proxys))
            sqlite = Sqlite(address + 'ip.db')
            sqlite.update_data('DELETE FROM ip_house')
            sqlite = Sqlite(address + 'ip.db')
            for i in range(len(proxys)):
                if proxys[i] and GetFreeProxy.verifyProxyFormat(proxys[i]):
                    sqlite.cursor.execute("INSERT INTO ip_house VALUES (?,?,?);", [i+1,proxys[i],'true'])
            sqlite.conn.commit()
            sqlite.close_conn()
        else:
            sqlite = Sqlite(address + 'ip.db')
            results = sqlite.query_data('select count(proxy_adress) from ip_house')
            if int(results[0][0]) == 0:
                proxys = GetFreeProxy.get_list_proxys()
                proxys = list(set(proxys))
                sqlite = Sqlite(address + 'ip.db')
                for i in range(len(proxys)):
                    if proxys[i] and GetFreeProxy.verifyProxyFormat(proxys[i]):
                        sqlite.cursor.execute("INSERT INTO ip_house VALUES (?,?,?);", [i + 1, proxys[i], 'true'])
                sqlite.conn.commit()
                sqlite.close_conn()

        sqlite = Sqlite(address + 'ip.db')
        results = sqlite.query_data('select id,proxy_adress from ip_house')
        params = []
        for result in results:
            param = str(result[0]) + '&&' + result[1]
            params.append(param)
        Log.v("发现ip代理数量:" + str(len(params)))
        Log.v('正在检查ip可用性...')
        if thread_or_process:
            GetFreeProxy.exec_multi_threading(pool_size,params)
        else:
            GetFreeProxy.exec_multi_process(pool_size,params)
        Log.v('更新完成')

    @staticmethod
    def get_list_proxys():
        proxys = []
        proxys.extend(GetFreeProxy.freeProxySecond())
        proxys.extend(GetFreeProxy.freeProxyFourth())
        proxys.extend(GetFreeProxy.freeProxyFifth())
        proxys.extend(GetFreeProxy.freeProxySixth())
        proxys.extend(GetFreeProxy.freeProxySeventh())
        proxys.extend(GetFreeProxy.freeProxyEight())
        proxys.extend(GetFreeProxy.freeProxyNinth())
        proxys.extend(GetFreeProxy.freeProxyTen())
        proxys.extend(GetFreeProxy.freeProxyEleven())
        proxys.extend(GetFreeProxy.freeProxyTwelve())
        proxys.extend(GetFreeProxy.freeProxyWallFirst())
        proxys.extend(GetFreeProxy.freeProxyWallSecond())
        proxys.extend(GetFreeProxy.freeProxyWallThird())
        return proxys

    @staticmethod
    def exec_multi_process(size, proxys):
        pool = multiprocessing.Pool(processes=size)
        for proxy in proxys:
            pool.apply_async(GetFreeProxy.validUsefulProxy, (proxy,))

        pool.close()
        pool.join()

    @staticmethod
    def exec_multi_threading(size, proxys):
        pool = threadpool.ThreadPool(size)

        reqs = threadpool.makeRequests(GetFreeProxy.validUsefulProxy, proxys)
        [pool.putRequest(req) for req in reqs]
        pool.wait()



if __name__ == '__main__':
    GetFreeProxy.getAllProxy()
    pass
