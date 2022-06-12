import mysql.connector
import secret

if secret.testBot:
    mydb = mysql.connector.connect(
        host=secret.testdbhost,
        user=secret.testdbusername,
        password=secret.testdbpassword,
        database=secret.testdb
    )
else:
    mydb = mysql.connector.connect(
        host=secret.livedbhost,
        user=secret.livedbusername,
        password=secret.livedbpassword,
        database=secret.livedb
    )

def get_member_data(memberid):
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM memberdata WHERE id = '{memberid}'")
    fetchedData = mycursor.fetchone()

    if fetchedData == None:
        sql = f"INSERT INTO memberdata (id, balance) VALUES ({memberid}, 0)"
        mycursor.execute(sql)
        mydb.commit()
        mycursor.execute(f"SELECT * FROM memberdata WHERE id = '{memberid}'")
        fetchedData = mycursor.fetchone()

    memberData = {}
    memberData["id"] = fetchedData[0]
    memberData["balance"] = fetchedData[1]
    if fetchedData[2] == "":
        memberData["inventory"] = []
    else:
        memberData["inventory"] = fetchedData[2].split(",")
    if fetchedData[3] == "":
        memberData["collection"] = []
    else:
        memberData["collection"] = fetchedData[3].split(",")
    memberData["email"] = fetchedData[4]

    if memberData["email"] == "":
        memberData["email"] = None

    return memberData

def write_member_data(member):
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
        
    mycursor = mydb.cursor()
    sql = f"UPDATE memberdata SET id = {member_id}, balance = {member_balance}, inventory = '{member_inventory}', collection = '{member_collection}', email = '{member_email}' WHERE id = {member_id}"
    mycursor.execute(sql)
    mydb.commit()