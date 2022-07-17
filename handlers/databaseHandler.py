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