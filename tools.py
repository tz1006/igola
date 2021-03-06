#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: tools.py
# version: 0.0.1
# description: igola.com tools





import requests
import random
import base64
from datetime import datetime, timedelta
from fake_useragent import UserAgent
from urllib.parse import urlencode


ua = UserAgent()

cabin_dict = {'E': 'Economy',
              'P': 'PremiumEconomy',
              'B': 'Business',
              'F': 'First'}


    
def airport_city_code(city):
    timestamp = get_timestamp()
    keyword = base64.b64encode(city.encode('utf-8')).decode('ascii')
    url = 'https://www.igola.com/web-gateway/api-data-service/data/find-airport?text=%s&lang=Wkg=&timestamp=%s' % (keyword, timestamp)
    with requests.session() as s:
        s.headers = {'accept': 'application/json, text/plain, */*',
                     'accept-encoding': 'gzip, deflate, br',
                     'accept-language': 'ZH',
                     'authorization': 'null',
                     'connection': 'close',
                     'guid': 'null',
                     'referer': 'https://www.igola.com/',
                     'user-agent': ua.random} 
        r = s.get(url)
    return r


# 获取城市代码
def city_code(city):
    r = airport_city_code(city)
    li = []
    l = len(r.json()['result'])
    if l >= 30:
        l = 30
    for i in range(0, l):
        code = r.json()['result'][i]['c']
        li.append(code)
    return li

# 获取机场代码
def airport_code(city):
    r = airport_city_code(city)
    li = []
    try:
        result = r.json()['result'][0]['s']
        for i in result:
            li.append(i['c'])
        return li
    except:
        li.append(r.json()['result'][0]['c'])
        return li

# 获取城市名
def city_name(code):
    r = airport_city_code(code)
    name = r.json()['result'][0]['ct']
    return name




# 生成-形式日期
def format_date(date):
    date = str(date)
    if '-' in date:
        return date
    else:
        y = date[:-4]
        m = date[-4:-2]
        d = date[-2:]
        if len(y) == 2:
            y = '20' + y
        date = '-'.join([y,m,d])
        return date

# 生成日期列表
def date_list(start_date, end_date):
    start_date = start_date.split('-')
    start_year = start_date[0]
    start_month = start_date[1]
    start_day = start_date[2]
    start_time = datetime.strptime('%s-%s-%s 09:25:00' % (start_year, start_month, start_day), "%Y-%m-%d %H:%M:%S")
    end_date = end_date.split('-')
    end_year = end_date[0]
    end_month = end_date[1]
    end_day = end_date[2]
    end_time = datetime.strptime('%s-%s-%s 09:25:00' % (end_year, end_month, end_day), "%Y-%m-%d %H:%M:%S")
    delta_days = (end_time.date() - start_time.date()).days
    li = []
    for i in range(delta_days+1):
        date = (start_time.date() + timedelta(days=i)).strftime("%Y-%m-%d")
        li.append(date)
    return li


# 获取时间戳
def get_timestamp(encode=0):
    t = datetime.now().timestamp()
    if encode == 0:
        timestamp = int(t * 1000)
    else:
        t=int(t)
        timestamp = 97 * t % 1000 + t * 1000
    return str(timestamp)

# 随机生成ip
def random_ip():
    ip = ".".join(map(str, (random.randint(0, 255)
                            for _ in range(4))))
    return ip

  

# 直飞城市
def direct_flight(city, date='', debug=0):
    if date != '':
        date = format_date(date)
    url = 'https://map.variflight.com/drx?_c=TTT'
    airport_list = airport_code(city)
    li = []
    for airport in airport_list:
        departcode = airport
        arrivecode = ''
        payload = urlencode(dict(
            queryDate1 = date,
            queryDate2 = date,
            alliance = '',
            dep = departcode,
            depType = 1,
            arr = arrivecode,
            arrType = 1,
            isDirect = 1,
            isStop = 0,
            isOwn =  1,
            isShare = 0,
            isConnect = 0,
            isDomestic = 1,
            isCross = 0))
        # print(payload)
        with requests.session() as s:
            s.headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                         'Accept-Encoding': 'gzip, deflate',
                         'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7',
                         'Connection': 'close',
                         'Content-Length': str(len(payload)),
                         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                         'Host': 'map.variflight.com',
                         'Origin': 'http://map.variflight.com',
                         'Referer': 'http://map.variflight.com/',
                         'User-Agent': ua.random,
                         'X-Requested-With': 'XMLHttpRequest'}
            code = 10
            while code != 0:
                r = s.post(url, data=payload)
                code = r.json()['code']
                if code != 0:
                    time.sleep(0.5)
        result = r.json()['data']
        for i in result:
            li.append(i[1])
    return li


