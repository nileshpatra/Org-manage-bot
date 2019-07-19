import sqlite3
connection = sqlite3.connect("meetings.db")

cursor = connection.cursor()

sql_command = """
CREATE TABLE meetup ( 
Date VARCHAR(30) PRIMARY KEY, 
Time VARCHAR(30),
Topic VARCHAR(30) 
);"""
cursor.execute(sql_command)

sql_command = """INSERT INTO meetup (Date, Time, Topic)
    VALUES ("29_may" , "5" , "kernel");"""
cursor.execute(sql_command)

connection.commit()
connection.close()
