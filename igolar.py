#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: igola/igolar.py
# discription: 

import requests
import json

ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'
ua_m = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B150 Safari/604.1'

header = {'User-Agent':ua, 'Content-Type': 'application/json', 'Referer' = 'https://www.igola.com/flights/ZH/lax-bjs_2018-03-22*2018-03-31_1*RT*Economy_0*0'}
s = requests.session()
s.keep_alive = False


# 创建sessionid
def create-session():
    url = 'https://www.igola.com/web-gateway/api-flight-polling-data-hub/create-session'
    payload = json.dumps({"lang":"ZH","queryObj":{"cabinAlert": False,"tripType":"RT","item":[{"from":{"c":"LAX","t":"C"},"to":{"c":"SHA","t":"C"},"date":"20180315"},{"from":{"c":"SHA","t":"C"},"to":{"c":"LAX","t":"C"},"date":"20180318"}],"passengerInfo":[],"cabinType":"Economy","isDomesticCabinType":0},"enableMagic":True,"magicEnabled":True})
    r = s.post(url, headers=header, data=payload)
    sessionid = r.json()['sessionId']
    return sessionid


def search()
url = 'https://www.igola.com/web-gateway/api-flight-polling-data-hub/packagedPolling'
payload = json.dumps({
"magicEnabled":true,
"currency":"CNY",
"lang":"ZH",
"filters":[],
"sorter":{},
"pageNumber":1,
"pageSize":20,
"sessionId":"a19dfda1-4e78-4569-a1c1-f32e00e1f3f0"}
