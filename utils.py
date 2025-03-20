import firebase_admin
from firebase_admin import credentials, firestore
import os

cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), 'my-money-flow-4fd41-firebase-adminsdk-fbsvc-ea9a5a5f5c.json'))
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_session():
    return db