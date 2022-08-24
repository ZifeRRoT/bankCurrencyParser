from pydantic import BaseModel


class Bank(BaseModel):
    id: int
    name: str
    mfo: int
    edrpou: int
    ipn: int
    iban: str
    swift: str

    class Config:
        orm_mode = True
