import mysql.connector
import secret
from definitions import Member

def create_connection():
    connection = mysql.connector.connect(
        host = secret.database.host,
        user = secret.database.user,
        password = secret.database.password,
        database = secret.database.database
    )

    return connection



def ensure_row_exists(cursor, member, create):
    memberID = member.id

    sql = f"SELECT * FROM memberdata WHERE id = {memberID}"

    cursor.execute(sql)
    result = cursor.fetchone()

    exists = (cursor.rowcount < 1)
    created = False

    if (not exists) and create:
        sql = f"INSERT INTO memberdata (id, balance, inventory, collection, counts) VALUES ({memberID}, 0, '', '', 0)"
        cursor.execute(sql)
        created = True

    return exists, created



def update_member_data(cursor, member):
    memberBalance = member.get_balance()
    memberInventory = ",".join(member.get_inventory())
    memberCollection = ",".join(member.get_collection())
    memberCounts = member.get_counts()
    memberID = member.id

    sql = f"UPDATE memberdata SET balance = {memberBalance}, inventory = '{memberInventory}', collection = '{memberCollection}', counts = {memberCounts} WHERE id = {memberID}"
    
    cursor.execute(sql)



def upload_all_members():
    connection = create_connection()
    cursor = connection.cursor()

    for member in Member.get_all_members():
        ensure_row_exists(cursor, member, True)
        update_member_data(cursor, member)

    connection.commit()