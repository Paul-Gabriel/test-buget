from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String

from constants import SCHEMA
from orm_models.base_model import BASE

class Users(BASE):
    __tablename__ = "user"
    __table_args__ = {"schema": SCHEMA}

    id = Column(Integer, primary_key=True, autoincrement=True)
    nume = Column(String(50))
    prenume = Column(String(50))
    email = Column(String(50), primary_key=True)
    parola = Column(String(50))
    venit = Column(Integer)

class Users_pydantic(BaseModel):
    nume: str
    prenume: str
    email:str
    parola:str
    venit:int

    def get_db_obj(self) -> Users:
        return Users(**self.model_dump())