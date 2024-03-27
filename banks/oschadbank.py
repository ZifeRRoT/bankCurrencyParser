from config import oschadbank_url
from tg_informer import send_error
from database import insert_to_db
import requests


@send_error
def start(header):
    result = {}
    request = requests.get(oschadbank_url, headers=header).json()
    items = dict(request['items'])
    for item in items:
        for i in items[item]:
            result.update({
                item: {
                    "purchase": float('{:.3f}'.format(float(items[item][i]['rate']['buy']))),
                    "sale": float('{:.3f}'.format(float(items[item][i]['rate']['sale'])))
                }
            })
    insert_to_db(300465, result)