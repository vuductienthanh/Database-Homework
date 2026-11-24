import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="...",
    database="taxi_homework"
)

if conn.is_connected():
    print("Connected to MariaDB successfully!")

conn.close()