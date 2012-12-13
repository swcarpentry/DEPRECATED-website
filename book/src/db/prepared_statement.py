import sys, sqlite3

statement = '''
SELECT PersonID, Project, Hours FROM Experiments WHERE PersonID = ? and Project = ?;
'''

connection = sqlite3.connect("lab.db")
cursor = connection.cursor()
for line in sys.stdin:
    person, project = line.strip().split(' ', 1)
    cursor.execute(statement, (person, project))
    results = cursor.fetchall();
    for r in results:
        print r
cursor.close()
connection.close()
