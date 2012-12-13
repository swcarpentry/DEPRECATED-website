import sqlite3

connection = sqlite3.connect("lab.db")
cursor = connection.cursor()
cursor.execute("SELECT PersonID, Email FROM Scientists;")
results = cursor.fetchall();
for r in results:
    print r
cursor.close();
connection.close();
