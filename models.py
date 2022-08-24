import sqlalchemy as sa

from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class BankList(Base):
    __tablename__ = "bank_list"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False, unique=True, index=True)
    mfo = sa.Column(sa.Integer, unique=True)
    edrpou = sa.Column(sa.Integer, unique=True)
    ipn = sa.Column(sa.BigInteger, unique=True)
    iban = sa.Column(sa.String, unique=True)
    swift = sa.Column(sa.String, unique=True)
    rates = relationship("ExchangeRates", backref="bank")


class Currency(Base):
    __tablename__ = "currency"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    code = sa.Column(sa.String, nullable=False, unique=True, index=True)
    name = sa.Column(sa.String, nullable=False, unique=True)
    rates = relationship("ExchangeRates", backref="currency")


class ExchangeRates(Base):
    __tablename__ = "exchange_rates"
    __table_args__ = (
        sa.UniqueConstraint("bank_id", "currency_id", "date", name="unique_exchange_rates"),
    )
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    bank_id = sa.Column(sa.Integer, sa.ForeignKey("bank_list.id"))
    currency_id = sa.Column(sa.Integer, sa.ForeignKey("currency.id"))
    purchase = sa.Column(sa.Float, nullable=False)
    sale = sa.Column(sa.Float, nullable=False)
    date = sa.Column(sa.Date, server_default=sa.func.now())
