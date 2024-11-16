import sqlite3

# Creates/opens a database file named 'parameter'
con = sqlite3.connect('key_value_store_database')
cur = con.cursor()
# create a table
cur.execute('''
    CREATE TABLE IF NOT EXISTS key_value (
    key,
    value,
    created-time, 
    updated-time)''')
            
res = cur.execute('SELECT name FROM sqlite_master')
            
res.fetchone()

# class SQL():
#     def __init__(self, sql, paramter):
        