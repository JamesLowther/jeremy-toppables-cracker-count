import sqlite3

DATABASE = "database.db"

def connect():
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    return (con, cur)
