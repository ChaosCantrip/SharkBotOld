from asyncore import write
import mysql.connector
import secret
from definitions import Member

if secret.testBot:
    db = secret.testdb
else:
    db = secret.maindb

def create_connection():
    mydb = mysql.connector.connect(
        host=db["host"],
        user=db["username"],
        password=db["password"],
        database=db["database"]
    )

    return mydb



def write_member_data(member, cursor):
    member_id = member.id
    member_balance = member.balance
    member_inventory = ""
    for item in member.inventory:
        member_inventory = member_inventory + item + ","
    member_inventory = member_inventory[:-1]
    member_collection = ""
    for item in member.collection:
        member_collection = member_collection + item + ","
    member_collection = member_collection[:-1]
    if member.linked_account == None:
        member_email = ""
    else:
        member_email = member.linked_account

    sql = f"UPDATE memberdata SET id = {member_id}, balance = {member_balance}, inventory = '{member_inventory}', collection = '{member_collection}', email = '{member_email}' WHERE id = {member_id}"
    cursor.execute(sql)



def upload_member_data(member):
    connection = create_connection()
    cursor = connection.cursor()

    write_member_data(member, cursor)

    connection.commit()
    connection.close()



def upload_all_data():
    connection = create_connection()
    cursor = connection.cursor()

    members = Member.get_all_members()

    for member in members:
        write_member_data(member, cursor)
    connection.commit()
    connection.close()
