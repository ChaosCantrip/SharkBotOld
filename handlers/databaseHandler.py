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



def update_member_data(cursor, member):
    memberBalance = member.get_balance()
    memberInventory = ",".join(member.get_inventory())
    memberCollection = ",".join(member.get_collection())
    memberCounts = member.get_counts()
    memberID = member.id

    sql = f"UPDATE memberdata SET balance = {memberBalance}, inventory = {memberInventory}, collection = {memberCollection}, counts = {memberCounts} WHERE id = {memberID}"
    
    cursor.execute(sql)



def upload_data():
    connection = create_connection()
    cursor = connection.cursor()

    for member in Member.get_all_members():
        update_member_data(cursor, member)

    connection.commit()