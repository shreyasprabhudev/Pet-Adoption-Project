import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'davyjones441'
)

cursorObject = dataBase.cursor()
cursorObject.execute("CREATE DATABASE pet_db")
print("All done!")