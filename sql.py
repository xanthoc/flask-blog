import sqlite3

dummy = [
	("Well", "I\'m well"),
	("Good", "I\'m good"),
	("Excellent", "I\'m excellent"),
	("Okay", "I\'m okay")
]

with sqlite3.connect("blog.db") as conn:
	c = conn.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS posts (title TEXT, post TEXT)")
	c.executemany("INSERT INTO posts VALUES(?, ?)", dummy)