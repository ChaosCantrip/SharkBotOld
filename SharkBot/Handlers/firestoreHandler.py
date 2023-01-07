import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import secret

_cred = credentials.Certificate("firebase.sbignore.json")

_app = firebase_admin.initialize_app(_cred)

db = firestore.client()

print("Firestore Client Initialised")

def update_data(member_id: int, member_data: dict):
    if secret.testBot:
        return
    doc_ref = db.collection(u"members")
    doc_ref.document(str(member_id)).set(member_data)
