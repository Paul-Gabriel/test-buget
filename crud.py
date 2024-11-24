from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from orm_models.buget import Buget
from orm_models.plati import Plata, Plata_pydantic
from orm_models.users import Users, Users_pydantic

# Creare utilizator
def create_user(session: Session, user: Users_pydantic):
    print("\tCreez un user")
    db_user = user.get_db_obj()
    try:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    except IntegrityError:
        session.rollback()
        raise ValueError("User with this email already exists")
        
# Obținerea unui utilizator după ID
def get_user_by_id(session: Session, user_id: int):
    print("\tIa un user dupa id")
    return session.query(Users).filter(Users.id == user_id).first()

# Obținerea unui utilizator după email
def get_user_by_email(session: Session, email: str):
    print("\tIa un user dupa email")
    return session.query(Users).filter(Users.email == email).first()

# Obținerea tuturor utilizatorilor
def get_users(session: Session, skip: int = 0, limit: int = 100):
    print("\tIa toti utilizatorii")
    return session.query(Users).offset(skip).limit(limit).all()

# Actualizare utilizator
def update_user(session: Session, user_id: int, user_data: Users_pydantic):
    print("\tActualizeaza un utilizator")
    db_user = session.query(Users).filter(Users.id == user_id).first()
    if db_user:
        db_user.nume = user_data.nume
        db_user.prenume = user_data.prenume
        db_user.email = user_data.email
        db_user.parola = user_data.parola
        db_user.venit = user_data.venit
        session.commit()
        session.refresh(db_user)
        return db_user
    return None

# Ștergere utilizator
def delete_user(session: Session, user_id: int):
    print("\tSterge un user dupa id")
    db_user = session.query(Users).filter(Users.id == user_id).first()
    if db_user:
        session.delete(db_user)
        session.commit()
        return db_user
    return None

# Creare buget
def create_buget(session: Session, user_id: int, procent_necesitati: float, procent_dorinte: float, procent_economii: float):
    print("\tCreeaza un buget")
    # Obținem utilizatorul din baza de date pentru a accesa venitul
    db_user = session.query(Users).filter(Users.id == user_id).first()
    
    if db_user is None:
        raise ValueError("Utilizatorul nu a fost gasit")
    
    if(procent_dorinte + procent_necesitati + procent_economii != 100):
        raise ValueError("Procentele nu insumeaza 100%")

    # Creăm bugetul și calculăm sumele pentru fiecare categorie pe baza veniturilor utilizatorului
    db_buget = Buget(
        user_id=user_id,
        necesitati=procent_necesitati,
        dorinte=procent_dorinte,
        economii=procent_economii,
    )
    
    session.add(db_buget)
    session.commit()
    session.refresh(db_buget)
    return db_buget

# Obținerea unui buget după user_id
def get_buget_by_user(session: Session, user_id: int):
    print("\tIa un buget dupa user_id")
    return session.query(Buget).filter(Buget.user_id == user_id).first()

# Actualizare buget
def update_buget(session: Session, user_id: int, necesitati: float, dorinte: float, economii: float):
    print("\tActualizeaza un buget")
    db_buget = session.query(Buget).filter(Buget.user_id == user_id).first()
    if db_buget:
        db_buget.necesitati = necesitati
        db_buget.dorinte = dorinte
        db_buget.economii = economii
        session.commit()
        session.refresh(db_buget)
        return db_buget
    return None

# Creare plată
def create_plata(session: Session, plata: Plata_pydantic):
    print("\tCreeaza o plata")
    db_plata = plata.get_db_obj()
    session.add(db_plata)
    session.commit()
    session.refresh(db_plata)
    return db_plata

# Obținerea plăților unui utilizator
def get_plati_by_user(session: Session, user_id: int, skip: int = 0, limit: int = 100):
    print("\tArata platile unui user dupa user_id")
    return session.query(Plata).filter(Plata.user_id == user_id).offset(skip).limit(limit).all()

# Obținerea unei plăți după ID
def get_plata_by_id(session: Session, plata_id: int):
    print("\tIa o plata dupa id")
    return session.query(Plata).filter(Plata.id == plata_id).first()

# Actualizare plată
def update_plata(session: Session, plata_id: int, suma: float, categorie: str, tip: str):
    print("\tActualizeaza o plata dupa id")
    db_plata = session.query(Plata).filter(Plata.id == plata_id).first()
    if db_plata:
        db_plata.suma = suma
        db_plata.categorie = categorie
        db_plata.tip = tip
        session.commit()
        session.refresh(db_plata)
        return db_plata
    return None

# Ștergere plată
def delete_plata(session: Session, plata_id: int):
    print("\tSterge o plata dupa id")
    db_plata = session.query(Plata).filter(Plata.id == plata_id).first()
    if db_plata:
        session.delete(db_plata)
        session.commit()
        return db_plata
    return None

def get_plati_pe_categorie(session: Session, user_id: int, categorie: str):
    print("\tAfisaza platile in functie de o categorie")
    # Obținem bugetul utilizatorului
    db_buget = session.query(Buget).filter(Buget.user_id == user_id).first()
    
    if not db_buget:
        raise ValueError(f"Nu există un buget pentru utilizatorul cu ID-ul {user_id}")
    
    # Verificăm dacă categoria este validă
    if categorie not in ['necesitate', 'dorință', 'economii']:
        raise ValueError("Categoria trebuie să fie 'necesitate', 'dorință' sau 'economii'")
    
    # Obținem plățile corespunzătoare categoriei din buget
    plati = session.query(Plata).filter(and_(
        Plata.user_id == user_id,
        Plata.categorie == categorie
        )).all()

    return plati
