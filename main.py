from typing import Union

import uvicorn

from utils import create_database, get_session
from api import app

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Name": "Paul Gabriel"}

# @app.post("/add_user")
# def add_user(user:Users_pydantic):
#     user_db = user.get_db_obj()
#     with get_session() as session:
#         session.add(user_db)
#         session.commit()
#         session.refresh(user_db)
#     return user_db.id

if __name__ == "__main__":
    create_database()
    uvicorn.run(app,host="127.0.0.1", port=8000)