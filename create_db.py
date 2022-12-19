import mysql.connector

my_db = mysql.connector.connect(host='localhost', user='root', password='')

cursor = my_db.cursor()

# cursor.execute("CREATE DATABASE users")

cursor.execute("SHOW DATABASES")

for db in cursor:
    print(db)
