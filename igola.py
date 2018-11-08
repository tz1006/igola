#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# filename: igola.py
# version: 0.0.1
# description: igola




import json
import time
from pprint import pprint
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed


# from tools import *

def roundtrip_polling(departCity, arrivalCity, departDate, returnDate, cabin='E', currency='CNY', debug=0):
session_url = 'https://www.igola.com/web-gateway/api-flight-polling-data-hub/create-session'
polling_url = 'https://www.igola.com/web-gateway/api-flight-polling-data-hub/packagedPolling'
departCode = city_code(departCity)[0]
arrivalCode = city_code(arrivalCity)[0]
departDate = format_date(departDate)
returnDate = format_date(returnDate)
departDateCode = ''.join(departDate.split('-'))
returnDateCode = ''.join(returnDate.split('-'))
cabinType = cabin_dict[cabin]
referer_url = 'https://www.igola.com/flights/timeline/ZH-CNY-1-RT-{}-0-0?trip={}-{}&date={}&trip2={}-{}&date2={}'.format(cabinType, departCode.lower(), arrivalCode.lower(), departDate, arrivalCode.lower(), departCode.lower(), returnDate)
#print(referer_url)
# session-payload
spayload = json.dumps({'lang': 'ZH',
'enableMagic': True,
'magicEnabled': True,
'adultAmount': 1,
'childAmount': 0,
'queryObj': {'cabinAlert': False,
'cabinType': cabinType,
'isDomesticCabinType': 0,
'item': [{'date': departDateCode,
'from': {'c': departCode, 't': 'C'},
'to': {'c': arrivalCode, 't': 'C'}},
{'date': returnDateCode,
'from': {'c': arrivalCode, 't': 'C'},
'to': {'c': departCode, 't': 'C'}}],
'passengerInfo': [],
'tripType': 'RT'}}).replace(' ', '')
with requests.session() as s:
# sheaders
s.headers = {'accept': 'application/json, text/plain, */*',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'ZH',
'authorization': 'null',
'content-length': str(len(spayload)),
'content-Type': 'application/json;charset=UTF-8',
'guid': 'null',
'igola-client': 'pc',
'origin': 'https://www.igola.com',
'referer': referer_url,
'timestamp': get_timestamp(encode=1),
'user-agent': ua.random}
sr = s.post(session_url, data=spayload)
resultCode = sr.json()['resultCode']
if resultCode != 200:
print('状态码1: %s' % resultCode)
return s.cookies, s.headers
sessionid = sr.json()['sessionId']
# DEBUG
if debug != 0:
print('DEBUG       CREATE-SESSION')
print('请求头：')
return(sr.request.headers)
print('载荷： %d' % len(spayload))
pprint(spayload)
# packagedPolling请求
payload = json.dumps({"currency": currency,
"lang":"ZH",
"sorters":[],
"filters":[],
"pageNumber":1,
"pageSize":30,
"sessionId":sessionid,
}).replace(' ', '')
s.headers['content-length'] = str(len(payload))
s.headers['session-id'] = sessionid
# print(s.headers)
r = s.post(polling_url, data=payload)
# time.sleep(0)
# r = s.post(polling_url, data=payload)
resultCode = r.json()['resultCode']
if resultCode != 200:
print('状态码2: %s' % resultCode)
# DEBUG
if debug != 0:
print('DEBUG       SINGLEPOLLING')
print('请求头：')
pprint(r.request.headers)
print('载荷： %d' % len(payload))
pprint(payload)
return r.json()



def roundtrip (departCity, arrivalCity, departDate, returnDate, stop=0, cabin='E', currency='CNY', debug=0):
r = roundtrip_polling(departCity, arrivalCity, departDate, returnDate, cabin='E', currency='CNY', debug)
prices = {0:None,1:None, 2:None}
for i in r['stopInfo']:
s = i['stops']
lowestPrice = int(i['lowestPrice'])
prices[s] = lowestPrice
result = []
for i in prices:
if i <= stop:
result.append(prices[i])
result.sort()
price = result[0]
stop = list(prices)[list(prices.values()).index(price)]
d['{}-{} {} {}-{}'.format(city_name(departCity), city_name(arrivalCity), stop, format_date(departDate), format_date(returnDate))] = price





def toCity(departCity, arrivalCity, departStartDate, departEndDate, returnStartDate, returnEndDate, stay=1,cabin='E'):
global d
d = {}
departStartDate = format_date(departStartDate)
departEndDate = format_date(departEndDate)
returnStartDate = format_date(returnStartDate)
returnEndDate = format_date(returnEndDate)
departcity = []
returncity = []
departlist = []
returnlist = []
cabinlist = []
departDatelist = date_list(departStartDate, departEndDate)
returnDatelist = date_list(returnStartDate, returnEndDate)
for i in departDatelist:
for l in returnDatelist:
a = int('%s%s%s' % (i.split('-')[0], i.split('-')[1], i.split('-')[2]))
b = int('%s%s%s' % (l.split('-')[0], l.split('-')[1], l.split('-')[2]))
if a < b:
date_diff = (datetime.strptime(l, '%Y-%m-%d') - datetime.strptime(i, '%Y-%m-%d')).days
if date_diff >= stay:
departcity.append(departCity)
returncity.append(arrivalCity)
departlist.append(i)
returnlist.append(l)
cabinlist.append(cabin)
print('执行%d次搜索' % len(cabinlist))
futures = []
with ThreadPoolExecutor(max_workers=200) as executor:
for i in range(len(cabinlist)):
futures.append(executor.submit(roundtrip, departcity[i], returncity[i], departlist[i], returnlist[i], stop=2, debug=1))
kwargs = {'total': len(futures)}
for f in tqdm(as_completed(futures), **kwargs):
pass
result = sorted(d.items(), key=lambda item: (item[1], item[0]))
return result






d = {}


r = toCity('lax', 'sha', '20181120', '20181124', '20181201', '20181203')

r = toCity('lax', 'sha', '20181120', '20181124', '20181201', '20190103')


r = roundtrip('lax', 'sha', 20181121,20181201,debug=0,stop=1)








class igola():
def __init__(self, city):
self.mycity =  city_code(city)[0]
self.mycityname = city_name(city)
self.destination = ['上海', '南京', '北京', '杭州', '武汉', '重庆', '天津', '长沙', '广州', '深圳','海口', '盐城', '南通', '三亚', '无锡', '厦门', '福州', '西安']
self.stop = 1
self.currency = 'CNY'
self.cabin = 'E'
self.stay = 1
self.debug = 0
self.max_workers = 200
self.d = {}
def roundtrip(self, departCity, arrivalCity, departDate, returnDate):
r = roundtrip_polling(departCity, arrivalCity, departDate, returnDate, cabin=self.cabin, currency=self.currency, debug=self.debug)
prices = {0:None,1:None, 2:None}
for i in r['stopInfo']:
s = i['stops']
lowestPrice = int(i['lowestPrice'])
prices[s] = lowestPrice
result = []
for i in prices:
if i <= self.stop:
result.append(prices[i])
result.sort()
price = result[0]
stop = list(prices)[list(prices.values()).index(price)]
key = '{}-{} {} {}-{}'.format(city_name(departCity), city_name(arrivalCity), stop, format_date(departDate), format_date(returnDate))
self.d[key] = price
def toCity(self, departCity, arrivalCity, departStartDate, departEndDate, returnStartDate, returnEndDate):
self.d = {}
departStartDate = format_date(departStartDate)
departEndDate = format_date(departEndDate)
returnStartDate = format_date(returnStartDate)
returnEndDate = format_date(returnEndDate)
departlist = []
returnlist = []
departDatelist = date_list(departStartDate, departEndDate)
returnDatelist = date_list(returnStartDate, returnEndDate)
for i in departDatelist:
for l in returnDatelist:
a = int('%s%s%s' % (i.split('-')[0], i.split('-')[1], i.split('-')[2]))
b = int('%s%s%s' % (l.split('-')[0], l.split('-')[1], l.split('-')[2]))
if a < b:
date_diff = (datetime.strptime(l, '%Y-%m-%d') - datetime.strptime(i, '%Y-%m-%d')).days
if date_diff >= self.stay:
departlist.append(i)
returnlist.append(l)
print('执行%d次搜索' % len(departlist))
futures = []
with ThreadPoolExecutor(self.max_workers) as executor:
for i in range(len(departlist)):
futures.append(executor.submit(self.roundtrip, departCity, arrivalCity, departlist[i], returnlist[i]))
kwargs = {'total': len(futures)}
for f in tqdm(as_completed(futures), **kwargs):
pass
result = sorted(self.d.items(), key=lambda item: (item[1], item[0]))
pprint(result)







lax = igola('lax')
#lax.roundtrip('lax', 'sha', 20181121,20181201)



lax.toCity('lax', 'sha', '20181215', '20181221', '20181201', '20190103')




lax.roundtrip('lax', 'sha', 20181121,20181201)
lax.d


