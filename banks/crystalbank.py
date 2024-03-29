import requests
import chrome
from bs4 import BeautifulSoup
from config import crystalbank_url
from tg_informer import send_error
from database import insert_to_db



@send_error
def start(header):
    result = {}
    # request = chrome.run_browser(crystalbank_url)
    request = requests.get(crystalbank_url, headers=header).text
    soup = BeautifulSoup(request, 'lxml')
    course_table = soup.find("table", class_="ratestb")
    table_tr = course_table.find_all("tr")
    for pair in table_tr[1:3]:
        pair = pair.find_all("td")
        name = pair[0].text
        purchase = float(pair[1].text.replace(",", "."))
        sale = float(pair[2].text.replace(",", "."))
        result.update({name: {"purchase": purchase, "sale": sale}})
    insert_to_db(339050, result)
    # print(result)