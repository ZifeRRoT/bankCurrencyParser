import chrome
from bs4 import BeautifulSoup
from config import oschadbank_url
from tg_informer import send_error
from database import insert_to_db


@send_error
def start(header):
    result = {}
    request = chrome.run_browser(oschadbank_url)
    soup = BeautifulSoup(request, 'lxml')
    course_table = soup.find("tbody", class_="heading-block-currency-rate__table-body")
    course_tr = course_table.find_all("tr")
    for i in course_tr:
        all_td = i.find_all("td")
        name = all_td[1].text
        if name == "HUF":
            continue
        purchase = float(all_td[3].text)/int(all_td[2].text)
        sale = float(all_td[4].text)/int(all_td[2].text)
        result.update({name: {"purchase": float('{:.3f}'.format(purchase)), "sale": float('{:.3f}'.format(sale))}})
    insert_to_db(300465, result)
    # print(result)