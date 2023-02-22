import os.path

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import SharkBot.Utils
import secret
import colorama
import logging

db_logger = logging.getLogger("firestore")
fake_logger = logging.getLogger("fake_db")

_FAKE_DB_FILEPATH = "data/live/fake_firestore"
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
        fake_logger.info(f"{collection}/{document} - File Write")
        SharkBot.Utils.FileChecker.directory(f"{_FAKE_DB_FILEPATH}/{collection}")
        SharkBot.Utils.JSON.dump(f"{_FAKE_DB_FILEPATH}/{collection}/{document}.json", data)
    db_logger.info(f"{collection}/{document} - Firestore upload")
    col_ref = db.collection(collection)
    doc_ref = col_ref.document(document)
    doc_ref.set(data)

def del_doc(collection: str, document: str) -> None:
    if secret.testBot:
        fake_logger.info(f"{collection}/{document} - File Delete")
        if os.path.isfile(f"{_FAKE_DB_FILEPATH}/{collection}/{document}.json"):
            os.remove(f"{_FAKE_DB_FILEPATH}/{collection}/{document}.json")
    db_logger.warning(f"{collection}/{document} - Firestore Delete")
    col_ref = db.collection(collection)
    doc_ref = col_ref.document(document)
    doc_ref.delete()
