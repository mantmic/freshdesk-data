import sqlite3

def getConnection(db_file):
    return(sqlite3.connect(db_file))
