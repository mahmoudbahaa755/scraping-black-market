from pydantic import BaseModel



class CurrencyExchange(BaseModel):
    from_currency: str
    to_currency: str
    amount: float

class Link(BaseModel):
    link: str

class Article(BaseModel):
    link: str