import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import secret
import colorama

_cred = credentials.Certificate("firebase.sbignore.json")
_app = firebase_admin.initialize_app(_cred)
db = firestore.client()
print(colorama.Fore.GREEN + colorama.Style.BRIGHT + "Firestore Client Initialised")

def upload_member_data(member_data: dict):
    set_doc(
        collection=u"members",
        document=member_data["id"],
        data=member_data
    )

def set_doc(collection: str, document: str, data: dict) -> None:
    if secret.testBot:
        return
    col_ref = db.collection(collection)
    doc_ref = col_ref.document(document)
    doc_ref.set(data)
