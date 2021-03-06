from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time


#所有行业代码
# [881148,
# 881129,881130,881166,881121,881138,881151,881134,
# 881123,881149,881136,881157,881124,881109,881119,
# 881133,881127,881117,881131,881118,881139,881120,
# 881102,881106,881155,881126,881110,881152,881163,
# 881107,881111,881122,881103,881144,881142,881159,
# 881158,881145,881105,881147,881164,881146,881116,
# 881143,881113,881115,881104,881128,881161,881132]


class AnalysisIndustry:
    def __init__(self):
        self.industry_codes = []
        
    def get_indusrty_codes(self):
        instury_index_url = 'http://q.10jqka.com.cn/thshy/'
        html = self.get_industry_list(instury_index_url)
        bs = BeautifulSoup(html, "html.parser")
        list = bs.find('tbody').find_all("a", target="_blank")  # 龙虎榜的stock
        print(type(list))
        print(len(list))
        for line in list:
            href = str((line.get('href')))
            if (href.find('thshy') == -1) is False:
                ret = href.split("/")[-2]
                self.industry_codes.append(ret)

    # 获取动态cookies
    def get_cookie(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        url = "http://q.10jqka.com.cn/thshy/"
        driver.get(url)
        # 获取cookie列表
        cookie = driver.get_cookies()
        driver.close()
        if len(cookie) > 0:
            return cookie[0]['value']
        return ''

    # 获取网页详情页
    def get_page_detail(self,url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Referer': 'http://q.10jqka.com.cn/thshy/detail',
            'Cookie': 'v={}'.format(self.get_cookie())
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.text.encode('utf-8')
            return None
        except RequestException:
            print('请求页面失败', url)
            return None

    # 获取行业列表 名称title、代码code、链接url
    def get_industry_list(self,url):
        html = self.get_page_detail(url)
        return (html)

    def get_all_data(self):
        with open('hys.txt', 'r', encoding='UTF-8') as f2:
            ls = f2.readlines()
            for l in ls:
                s = l.replace('\n','').split(' ')
                code = s[0]
                data = self.get_one_data(str(code))
                with open('hangye/'+ s[1]+'.txt', 'w') as f:
                    f.write(str(data))
                time.sleep(5)
                print(code)

    def get_one_data(self,code_industry):
        url = 'http://d.10jqka.com.cn/v4/line/bk_' + code_industry + '/21/last.js'
        html = self.get_page_detail(url).decode('gbk')
        return html

if __name__ == '__main__':
    s = AnalysisIndustry()
    # s.get_indusrty_codes()
    # s.get_all_data()
    # print(s.get_one_data('881131'))
    with open('all_industry_data.txt', 'r', encoding='UTF-8') as f1:
        fs = f1.read()
        with open('hys.txt', 'r', encoding='UTF-8') as f2:
            ls = f2.readlines()
            for l in ls:
                s = l.replace('\n','').split(' ')[0]
                if s not in fs:
                    print(s)