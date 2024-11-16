import sqlite3
# documentation: https://docs.python.org/3/library/sqlite3.html
# Creates/opens a database file named 'parameter'
con = sqlite3.connect('key_value_store_database')
# Create a cursor
cur = con.cursor()
# create a table
cur.execute('''
    CREATE TABLE IF NOT EXISTS key_value (
    key,
    value,
    created_time, 
    updated_time
    )
''')
            
res = cur.execute('SELECT key FROM key_value')

print(res.fetchone())

class SQL():

    def __init__(self, sql, paramters):
        self.sql = sql
        self.parameters = paramters
        
    def init_table(self, db_name):
        # Creates/opens a database file named 'parameter'
        con = sqlite3.connect('key_value_store_database')
        # Create a cursor
        cur = con.cursor()
        # create a table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS key_value (
            key,
            value,
            created_time, 
            updated_time
            )
        ''')
    

    