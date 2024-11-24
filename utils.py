from sqlalchemy import Inspector, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema

from constants import HOST, PASSWORD, PORT, SCHEMA, USER
from orm_models.base_model import BASE

def get_engine():
    return create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}")

def get_session():
    session = sessionmaker(bind = get_engine())
    return session()

def does_schema_exist(schema_name:str):
    engine = get_engine()
    return schema_name.lower() in Inspector(engine).get_schema_names()

def create_schema(schema_name):
    if does_schema_exist(schema_name):
        print(f"{schema_name} schema already exists")
        return False
    with get_session() as session:
        session.execute(CreateSchema(schema_name))
        return True

def create_database():
    try:
        create_schema(SCHEMA)
        BASE.metadata.create_all(get_engine())
        return True
    except Exception as e:
        print(e)
        return False