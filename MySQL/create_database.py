import mysql.connector

#mysql> CREATE DATABASE test
mysql_connection = mysql.connector.connect(user = 'root', password = 'Laijiachong1', host = 'localhost',charset ='utf8' )
cursor = mysql_connection.cursor()
cursor.execute('CREATE DATABASE crawler charset=utf8')
#mycursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
#mycursor.execute("CREATE DATABASE test")
#mycursor.execute("SHOW DATABASES")
#for x in mycursor:
#      print(x)

