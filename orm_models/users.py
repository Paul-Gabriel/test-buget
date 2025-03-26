from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL

from constants import SCHEMA
from orm_models.base_model import BASE

class Users(BASE):
    __tablename__ = "user"
    __table_args__ = {"schema": SCHEMA}

    id = Column(Integer, primary_key=True, autoincrement=True)
    nume = Column(String(50))
    prenume = Column(String(50))
    email = Column(String(50), unique=True)
    parola = Column(String(50))
    venit = Column(Integer)
    procentNecesitati = Column(Integer)
    procentDorinte = Column(Integer)
    procentEconomii = Column(Integer)

class Users_pydantic(BaseModel):
    id: int
    nume: str
    prenume: str
    email:str
    parola:str
    venit:int
    procentNecesitati:int
    procentDorinte:int
    procentEconomii:int

    def get_db_obj(self) -> Users:
        return Users(**self.model_dump())