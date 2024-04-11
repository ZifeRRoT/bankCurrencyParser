import requests
import chrome
from bs4 import BeautifulSoup
from config import ukreximbank_url
from tg_informer import send_error
from datetime import datetime
from database import insert_to_db



# @send_error
def start(header):
    result = {}
    request = requests.get(ukreximbank_url, headers=header).json()
    items = list(request['rates']['cash']['data'])
    for i in items:
        if not bool(int(i['buy'].replace(',', ''))) or not bool(int(i['buy'].replace(',', ''))):
            continue
        result.update({i['code']:{
            "purchase": float('{:.3f}'.format(float(i['buy'].replace(',', '.')))),
            "sale": float('{:.3f}'.format(float(i['sell'].replace(',', '.'))))
        }})
    insert_to_db(322313, result)