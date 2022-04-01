import mysql.connector
mysql_connection = mysql.connector.connect(user = 'root', password = 'Laijiachong1', host = 'localhost',database = 'crawler' )
cursor = mysql_connection.cursor()

sql_insert = "INSERT INTO results_1 (Titles) VALUES (%s)"
sql_delete = "DELETE FROM results"
sql_order = 'SELECT * FROM results_1 ORDER BY Titles DESC;'
results_1 =[('test_title')]
results_2 = [('a')]
results_3 = [('b')]

cursor.execute(sql_insert, results_1)
cursor.execute(sql_insert, results_2)
cursor.execute(sql_insert, results_3)
mysql_connection.commit()
cursor.execute(sql_order)
order = cursor.fetchall()
for i in order:
    print(i)
    cursor.execute('INSERT INTO results_2 (Titles) VALUES (%s)',i)
    mysql_connection.commit()
    




