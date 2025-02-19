from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from orm_models.plati import Plata_pydantic
from orm_models.users import Users_pydantic
from utils import get_session

app = FastAPI()


@app.post("/users/")
def create_user(user: Users_pydantic, session = Depends(get_session)):
    return crud.create_user(session=session, user=user)

@app.get("/users/{user_id}")
def get_user(user_id: int, session = Depends(get_session)):
    db_user = crud.get_user_by_id(session=session, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/email/{email}")
def get_user(email: str, session = Depends(get_session)):
    db_user = crud.get_user_by_email(session=session, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/")
def get_users(skip: int = 0, limit: int = 100, session = Depends(get_session)):
    users = crud.get_users(session=session, skip=skip, limit=limit)
    return users

@app.put("/users/{user_id}")
def update_user(user_id: int, user: Users_pydantic, session = Depends(get_session)):
    db_user = crud.update_user(session=session, user_id=user_id, user_data=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, session = Depends(get_session)):
    db_user = crud.delete_user(session=session, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}

@app.post("/plata/")
def create_plata(plata: Plata_pydantic, session = Depends(get_session)):
    return crud.create_plata(session=session, plata=plata)

@app.get("/plati/{user_id}")
def get_plati(user_id: int, session = Depends(get_session)):
    return crud.get_plati_by_user(session=session, user_id=user_id)

@app.get("/plata/{plata_id}")
def get_plata(user_id: int, plata_id: int, session = Depends(get_session)):
    db_plata = crud.get_plata_by_id(session=session,user_id=user_id, plata_id=plata_id)
    if db_plata is None:
        raise HTTPException(status_code=404, detail="Plata not found")
    return db_plata

@app.put("/plata/{plata_id}")
def update_plata(user_id: int,plata_id: int, plata: Plata_pydantic, session = Depends(get_session)):
    db_plata = crud.update_plata(session=session,user_id=user_id, plata_id=plata_id, plata_data=plata)
    if db_plata is None:
        raise HTTPException(status_code=404, detail="Plata not found")
    return db_plata

@app.delete("/plata/{plata_id}")
def delete_plata(user_id: int, plata_id: int, session = Depends(get_session)):
    db_plata = crud.delete_plata(session=session,user_id=user_id, plata_id=plata_id)
    if db_plata is None:
        raise HTTPException(status_code=404, detail="Plata not found")
    return {"detail": "Plata deleted"}

@app.get("/plati/{user_id}/{categorie}")
def get_plati(user_id: int, categorie: str, session = Depends(get_session)):
    try:
        plati = crud.get_plati_pe_categorie(session=session, user_id=user_id, categorie=categorie)
        return plati
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))