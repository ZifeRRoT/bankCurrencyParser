import requests
from bs4 import BeautifulSoup
from config import privatbank_url
from tg_informer import send_error
from database import insert_to_db


@send_error
def start(header):
    result = {}
    request = requests.get(url=privatbank_url, headers=header)
    soup = BeautifulSoup(request.text, 'lxml')
    course_table = soup.find("div", class_="courses-currencies")
    currency_pairs = course_table.find_all("div", class_="currency-pairs")
    for pair in currency_pairs:
        name = pair.find("span").text.split()[0]
        purchase = float(pair.find("div", class_="purchase").text.strip())
        sale = float(pair.find("div", class_="sale").text.strip())
        result.update({name: {"purchase": purchase, "sale": sale}})
    insert_to_db(14360570, result)
