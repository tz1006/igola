#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: travelpayouts.py
# version: 0.0.1
# description: travelpayouts




import json
import time
from pprint import pprint
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests



s = requests.session()
s.

url = 'http://min-prices.aviasales.ru/calendar_preload?origin=LAX&destination=SHA&depart_date=2018-11-21&return_date=2018-12-01&one_way=false'
