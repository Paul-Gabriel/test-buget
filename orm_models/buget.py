from pydantic import BaseModel
from sqlalchemy import DECIMAL, Column, ForeignKey, Integer, String

from constants import SCHEMA
from orm_models.base_model import BASE
from orm_models.users import Users

class Buget(BASE):
    __tablename__ = "buget"
    __table_args__ = {"schema": SCHEMA}

    user_id = Column(Integer, ForeignKey(Users.id), primary_key=True)
    necesitati = Column(DECIMAL(10, 2))
    dorinte = Column(DECIMAL(10, 2))
    economii = Column(DECIMAL(10, 2))

class Buget_pydantic(BaseModel):
    tip_buget:str

    def get_db_obj(self) -> Buget:
        return Buget(**self.model_dump())