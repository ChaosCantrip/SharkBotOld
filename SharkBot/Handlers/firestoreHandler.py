import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import SharkBot

_cred = credentials.Certificate("firebase.sbignore.json")

_app = firebase_admin.initialize_app(_cred)

db = firestore.client()

print("Firestore Client Initialised")