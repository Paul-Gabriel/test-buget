import firebase_admin
from firebase_admin import credentials, firestore
import os

cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), 'test-44edc-firebase-adminsdk-cakyn-75aec87cb6.json'))
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_session():
    return db