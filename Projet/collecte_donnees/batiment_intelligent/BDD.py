import mysql.connector

def connection_BDD():
    conn = mysql.connector.connect(
        host='192.168.20.61',
        user='ludo',
        password='root',
        database='batiment_intelligent'
    )
    return conn

