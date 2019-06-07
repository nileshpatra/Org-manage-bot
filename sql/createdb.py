import sqlite3
connection = sqlite3.connect("filter.db")

cursor = connection.cursor()

sql_command = """
CREATE TABLE message ( 
keyword VARCHAR(30) PRIMARY KEY, 
response VARCHAR(30) 
);"""
cursor.execute(sql_command)

sql_command = """INSERT INTO message (keyword, response)
    VALUES ("1" , "first commit");"""
cursor.execute(sql_command)

connection.commit()
connection.close()