import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('firestorecred.sbignore.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


def upload_member(data: dict):
    doc_ref = db.collection(u'memberdata').document(str(data["id"]))
    doc_ref.set(data)
