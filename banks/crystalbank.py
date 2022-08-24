import requests
from bs4 import BeautifulSoup
from datetime import date
from config import crystalbank_url
from tg_informer import send_error


@send_error
def start(header):
    today = str(date.today())
    result = {"date": today}
    request = requests.get(url=crystalbank_url, headers=header)
    soup = BeautifulSoup(request.text, 'lxml')
    course_table = soup.find("div", class_="carousel-entry-big-subtitle")
    table_tr = course_table.find_all("tr")
    for pair in table_tr[2:4]:
        pair = pair.find_all("td")
        name = pair[0].text
        purchase = float(pair[1].text.replace(",", "."))
        sale = float(pair[2].text.replace(",", "."))
        result.update({name: {"purchase": purchase, "sale": sale}})
    send_to_db("crystalbank", result)
