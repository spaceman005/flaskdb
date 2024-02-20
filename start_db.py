import sqlite3

connection = sqlite3.connect("user_data.db")
cursor = connection.cursor()
command = """CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT)"""
command2 = """CREATE TABLE IF NOT EXISTS post(id INTEGER PRIMARY KEY AUTOINCREMENT, author_id INTEGER NOT NULL, created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, title TEXT NOT NULL, body TEXT NOT NULL, FOREIGN KEY (author_id) REFERENCES user (id))"""
cursor.execute(command2)

#cursor.execute("INSERT INTO users VALUES ('ethan', '1234')")
#connection.commit()