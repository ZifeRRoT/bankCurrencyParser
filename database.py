import os

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, insert
from models import *
from dotenv import load_dotenv
from schemas import *


load_dotenv()
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_host = os.environ.get("DB_HOST")
db_name = os.environ.get("DB_NAME")

DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"


engine = create_engine(DATABASE_URL)
session = Session(engine, future=True, autocommit=False, autoflush=False)


def insert_to_db(edrpou: int, data: dict):
    bank = session.execute(select(BankList).filter_by(edrpou=edrpou)).scalar_one()
    for key in data:
        currency = session.execute(select(Currency).filter_by(code=key)).scalar_one()
        exchange = ExchangeRates(
            purchase=data[key]['purchase'],
            sale=data[key]['sale'],
            bank=bank,
            currency=currency
        )
        session.add(exchange)
    session.commit()
