import sqlite3
# documentation: https://docs.python.org/3/library/sqlite3.html
# Creates/opens a database file named 'parameter'

class DatabaseManager():

    def __init__(self, db_name = 'default_name'):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self._init_db()
        self._init_table()


    def _init_db(self):
        # Creates/opens a database connection to an SQLite database named 'parameter'
        self.connection = sqlite3.connect(self.db_name, timeout=5.0)
        self.cursor = self.connection.cursor()
    
    def _init_table(self):
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.db_name}(
            key TEXT,
            value TEXT,
            created_time REAL, 
            updated_time REAL
            )
        ''') #REAL -> float / TEXT -> String
        print('table created!')
        
    def push_data(self, sql, parameters= None):
        try:
            result = self.cursor.executemany(
                f'''
                {sql},
                {parameters}
                    ''')
            self.connection.commit()
            
            return result.fetchall()
        
        except sqlite3.Error as e:
            print(f"Query error: {e}")
            self.connection.rollback()
            raise


    def show_data(self):
        res = self.cursor.execute(self.sql)
        print(res)



    def close(self):
        if self.connection:
            self.connection.close()
        if self.cursor:
            self.cursor.close()