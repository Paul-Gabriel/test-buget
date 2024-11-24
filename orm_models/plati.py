from pydantic import BaseModel
from sqlalchemy import DECIMAL, TIMESTAMP, Column, ForeignKey, Integer, String

from constants import SCHEMA
from orm_models.base_model import BASE
from datetime import date

from orm_models.users import Users


class Plata(BASE):
    __tablename__ = 'plati'
    __table_args__ = {"schema": SCHEMA}


    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(Users.id))
    suma = Column(DECIMAL(10, 2))
    categorie = Column(String(50))  # 'necesitate', 'dorință', 'economii'
    tip = Column(String(50))
    data = Column(TIMESTAMP)


class Plata_pydantic(BaseModel):
    user_id:int
    suma:float
    categorie:str
    tip:str
    data: date

    def get_db_obj(self) -> Plata:
        return Plata(**self.model_dump())
    