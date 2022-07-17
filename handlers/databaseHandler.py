import mysql.connector
import secret

def create_connection():
    connection = mysql.connector.connect(
        host = secret.database.host,
        user = secret.database.user,
        password = secret.database.password,
        database = secret.database.database
    )

    return connection