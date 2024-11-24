from sqlalchemy.orm import DeclarativeBase

class BASE(DeclarativeBase):
    def __repr__(self) -> str:
        return self.__tablename__
    
    