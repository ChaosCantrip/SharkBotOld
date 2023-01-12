import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import secret
import colorama

if not secret.testBot:
    _cred = credentials.Certificate("firebase.sbignore.json")
    _app = firebase_admin.initialize_app(_cred)
    db = firestore.client()
    print(colorama.Fore.GREEN + colorama.Style.BRIGHT + "Firestore Client Initialised")
else:
    print(colorama.Fore.YELLOW + colorama.Style.BRIGHT + "Firestore Client Ignored (Test Bot)")

def upload_data(member_data: dict):
    if secret.testBot:
        return
    doc_ref = db.collection(u"members")
    doc_ref.document(member_data["id"]).set(member_data)
