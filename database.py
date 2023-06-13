import os

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from sqlalchemy.dialects.postgresql import insert
from models import *
from dotenv import load_dotenv


load_dotenv()
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_host = os.environ.get("DB_HOST")
db_name = os.environ.get("DB_NAME")

DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"


engine = create_engine(DATABASE_URL, future=True)
session = Session(engine, future=True, autocommit=False, autoflush=False)


def insert_to_db(mfo: int, data: dict):
    bank = session.execute(select(BankList).filter_by(mfo=mfo)).scalar_one()
    for key in data:
        currency = session.execute(select(Currency).filter_by(code=key)).scalar_one()
        insert_exchange = insert(ExchangeRates).values(
            purchase=data[key]['purchase'],
            sale=data[key]['sale'],
            bank_id=bank.id,
            currency_id=currency.id
        )
        upd_exchange = insert_exchange.on_conflict_do_update(
            constraint='unique_exchange_rates',
            set_=dict(purchase=data[key]['purchase'], sale=data[key]['sale'])
        )
        session.execute(upd_exchange)
    session.commit()
