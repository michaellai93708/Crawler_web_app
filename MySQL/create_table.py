import mysql.connector
mysql_connection = mysql.connector.connect(user = 'root', password = 'Laijiachong1', host = 'localhost',database = 'crawler' )
cursor = mysql_connection.cursor()

cursor.execute('CREATE TABLE bid_id (bid_id VARCHAR(255), keyword VARCHAR(255))')


