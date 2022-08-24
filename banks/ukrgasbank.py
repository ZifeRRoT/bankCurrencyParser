import chrome
from bs4 import BeautifulSoup
from config import ukrgasbank_url
from tg_informer import send_error
from database import insert_to_db


@send_error
def start(header):
    names = {
        "100 Доларів США": "USD",
        "100 Євро": "EUR",
        "100 Швейцарських франків": "CHF",
        "100 Польських злотих": "PLN",
        "100 Англійських фунтів": "GBP",
        "100 чеських крон": "CZK"
    }

    result = {}
    request = chrome.run_browser(ukrgasbank_url)
    soup = BeautifulSoup(request, 'lxml')
    course_table = soup.find("div", class_="kurs-full")
    course_tr = course_table.find_all("tr")
    for i in course_tr[1:7]:
        all_td = i.find_all("td")
        name = names[all_td[1].text]
        purchase = float(all_td[2].text)/100
        sale = float(all_td[3].text)/100
        result.update({name: {"purchase": purchase, "sale": sale}})
    insert_to_db(23697280, result)
