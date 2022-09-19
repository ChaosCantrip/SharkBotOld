import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import secret


if secret.allowFirestore:
    cred = credentials.Certificate('firestorecred.sbignore.json')
    firebase_admin.initialize_app(cred)

    db = firestore.client()


def upload_member(data: dict):
    if secret.allowFirestore:
        return
    doc_ref = db.collection(u'memberdata').document(str(data["id"]))
    doc_ref.set(data)
