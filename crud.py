from sqlalchemy import and_
from sqlalchemy.orm import Session
from firebase_admin import firestore

from orm_models.plati import Plata, Plata_pydantic
from orm_models.users import Users, Users_pydantic

# Creare utilizator
def create_user(session, user: Users_pydantic):
    print("\tCreaza un user")

    if(user.dorinte + user.necesitati + user.economii != 100):
        raise ValueError("Procentele nu insumeaza 100%")
    
    if(get_user_by_email(session, user.email)):
        raise ValueError("Email-ul exista deja")

    user_data = user.dict()
    users_ref = session.collection('users')
    last_user = users_ref.order_by('id', direction=firestore.Query.DESCENDING).limit(1).stream()
    last_id = -1
    for doc in last_user:
        last_id = doc.to_dict().get('id', 0)
    new_id = last_id + 1
    user_data['id'] = new_id
    user_ref = users_ref.document(str(user_data['id']))
    user_ref.set(user_data)
    return user_data

# Obținerea unui utilizator după ID
def get_user_by_id(session, user_id: int):
    print("\tIa un user dupa id")
    users_ref = session.collection('users')
    query = users_ref.where('id', '==', user_id).stream()
    for doc in query:
        return doc.to_dict()
    return None

# Obținerea unui utilizator după email
def get_user_by_email(session, email: str):
    print("\tIa un user dupa email")
    # return session.query(Users).filter(Users.email == email).first()
    users_ref = session.collection('users')
    query = users_ref.where('email', '==', email).stream()
    for doc in query:
        return doc.to_dict()
    return None

# Obținerea tuturor utilizatorilor
def get_users(session, skip: int = 0, limit: int = 100):
    print("\tArata toti userii")
    users_ref = session.collection('users')
    users = [doc.to_dict() for doc in users_ref.stream()]
    return users[skip:skip+limit]

# Actualizare utilizator
def update_user(session, user_id: int, user_data: Users_pydantic):
    print("\tActualizeaza un user dupa id")
    users_ref = session.collection('users')
    query = users_ref.where('id', '==', user_id).stream()
    for doc in query:
        user_ref = session.collection('users').document(doc.id)
        user_ref.update(user_data.dict())
        return user_data.dict()
    return None

# Ștergere utilizator
def delete_user(session, user_id: int):
    print("\tSterge un user dupa id")
    
    plati_ref = session.collection('plati'+str(user_id))
    plati = [doc.to_dict() for doc in plati_ref.stream()]
    for plata in plati:
        delete_plata(session, plata['user_id'], plata['id'])

    users_ref = session.collection('users')
    query = users_ref.where('id', '==', user_id).stream()
    for doc in query:
        user_ref = session.collection('users').document(doc.id)
        user_ref.delete()
        return doc.to_dict()
    return None

# Creare plată
def create_plata(session: Session, plata: Plata_pydantic):
    print("\tCreeaza o plata")
    plata_data = plata.dict()
    plati_ref = session.collection('plati'+str(plata_data['user_id']))
    last_plata = plati_ref.order_by('id', direction=firestore.Query.DESCENDING).limit(1).stream()
    last_id = -1
    for doc in last_plata:
        last_id = doc.to_dict().get('id', 0)
    new_id = last_id + 1
    plata_data['id'] = new_id
    plata_ref = plati_ref.document(str(plata_data['id']))
    plata_ref.set(plata_data)
    return plata_data

# Obținerea plăților unui utilizator
def get_plati_by_user(session: Session, user_id: int, skip: int = 0, limit: int = 100):
    print("\tArata platile unui user dupa user_id")
    plati_ref = session.collection('plati'+str(user_id))
    plati = [doc.to_dict() for doc in plati_ref.stream()]
    return plati[skip:skip+limit]

# Obținerea unei plăți după ID
def get_plata_by_id(session: Session,user_id:int, plata_id: int):
    print("\tIa o plata dupa id")
    plati_ref = session.collection('plati'+str(user_id))
    query = plati_ref.where('id', '==', plata_id).stream()
    for doc in query:
        return doc.to_dict()
    return None

# Actualizare plată
def update_plata(session: Session, user_id:int, plata_id: int, plata_data: Plata_pydantic):
    print("\tActualizeaza o plata dupa id")
    plata_ref = session.collection('plati'+str(user_id))
    query = plata_ref.where('id', '==', plata_id).stream()
    for doc in query:
        plata_ref = session.collection('plati'+str(user_id)).document(doc.id)
        plata_ref.update(plata_data.dict())
        return plata_data.dict()
    return None

# Ștergere plată
def delete_plata(session: Session, user_id: int, plata_id: int):
    print("\tSterge o plata dupa id")
    plata_ref = session.collection('plati'+str(user_id))
    query = plata_ref.where('id', '==', plata_id).stream()
    for doc in query:
        plata_ref = session.collection('plati'+str(user_id)).document(doc.id)
        plata_ref.delete()
        return doc.to_dict()
    return None

def get_plati_pe_categorie(session: Session, user_id: int, categorie: str):
    print("\tAfisaza platile in functie de o categorie")
    # Obținem bugetul utilizatorului
    plati_ref = session.collection('plati'+str(user_id))
    plati = [doc.to_dict() for doc in plati_ref.where('categorie', '==', categorie).stream()]
    return plati
