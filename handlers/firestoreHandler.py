import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from definitions import Member

# Use a service account
cred = credentials.Certificate('firestorecred.sbignore.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


def upload_member(member: Member.Member):
    doc_ref = db.collection(u'memberdata').document(str(member.id))
    doc_ref.set({
        u"id": member.id,
        u"balance": member.balance,
        u"inventory": member.get_inventory(),
        u"collection": member.get_collection(),
        u"counts": member.get_counts()
    })
