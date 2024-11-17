import sqlite3
# documentation: https://docs.python.org/3/library/sqlite3.html
# Creates/opens a database file named 'parameter'

class DatabaseManager():

    def __init__(self, db_name ='default_name'):
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
            CREATE TABLE IF NOT EXISTS key_value_store(
            key TEXT,
            value TEXT,
            created_datetime REAL, 
            updated_datetime REAL
            )
        ''') #REAL -> float / TEXT -> String
        self.connection.commit()
        print('table created!', '-'*100)
        self.cursor.execute(f'PRAGMA table_info({self.db_name})')
        columns = self.cursor.fetchall()

    # call when action == INSERT
    def push_data(self, sql, parameters= None):
        try:
            if parameters is None:
                raise ValueError("Parameters connot be None")
            
            if isinstance(parameters, (list, tuple)):

                if len(parameters) == 2:
                    self.cursor.execute(sql, parameters)
                    self.connection.commit()
                    print(f"Single record inserted: {parameters}")
            else:
                raise ValueError("Parameters must be a list/tuple with exactly 2 values")
            return True
        
        except sqlite3.Error as e:
            print(f"Query error: {e}")
            self.connection.rollback()
            raise

    # call when action == 'UPDATE'
    def update_data(self, sql, parameters= None):
        try:
            if parameters is None: #check if returns correctly
                raise ValueError("Parameters connot be None")
            
            if isinstance(parameters, (list, tuple)):
                if len(parameters) == 2: # check if returns has two parameter
                    self.cursor.execute(sql, parameters)
                    self.connection.commit()
                    print(f"New record added: {parameters[1]} == {parameters[0]}")
            else:
                raise ValueError('Paramters must a list/tuple with exactly 2 values')
            
            if self.cursor.rowcount == 0: #this is to check if there is any modification in cursor to know if there is the specified value to update, if cursor.rowcount == 0 that means there is nothing to update and should raise an error
                print(f"No record found with key: {parameters[1]}. Use add_value instead.")
                raise ValueError(f"Key {parameters[1]} not found")
            else:
                print(f"Successfully updated value for key {parameters[1]}")

        except sqlite3.Error as e:
            print(f"Update error: {e}")
            self.connection.rollback()
            raise

    # call when action == SELECT
    def select_data(self, sql, parameters):
        try:
            if parameters is None:
                raise ValueError('Parameters cannot be None')

            if isinstance(parameters, (list, tuple)):

                if len(parameters) == 1:
                    self.cursor.execute(sql, parameters)
                    results = self.cursor.fetchall()
                    if results:
                        print(f"data_selected: {results[0]}")
                    # if results:
                    #     print(f'''
                    #     Key: {results[0]}
                    #     Value: {results[1]}
                    #     Created: {results[2]}
                    #     Updated: {results[3]}
                    #     ''')
                    #     return results
                    else:
                        print('No result found')
                        return None

        except sqlite3.Error as e:
            print(f"Error: {e}")

    #call when action == 'DELETE'
    def delete_data(self, sql, parameters):
        try:
            if parameters is None:
                raise ValueError('Parameters cannot be None')

            if isinstance(parameters, (list, tuple)):

                if len(parameters) == 1:
                    self.cursor.execute(sql, parameters)
                    self.connection.commit()

                    if self.cursor.rowcount == 0: #this is to check if there is any modification in cursor to know if there is the specified value to delect, if cursor.rowcount == 0 that means there is nothing to delect and should raise an error
                        print(f"No record found with key: {parameters}")
                        return False
                    print(f"Successfully delected key: {parameters}")

        except sqlite3.Error as e:
            print(f"Delete error: {e}")
            self.connection.rollback()
            raise

    #call when action == 'DELETE_ALL'    
    def delete_all(self, sql):
        try:

            self.cursor.execute(sql)

            self.connection.commit()
            print(f"Delected all {self.cursor.rowcount} records")
            return self.cursor.rowcount
        
        except sqlite3.Error as e:
            print(f"Delete error: {e}")
            self.connection.rollback()
            raise     

    def show_data(self):
        try:
            self.cursor.execute("SELECT * FROM key_value_store")
            results = self.cursor.fetchall()
            
            for row in results:
                print(row)

            return results
        
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            self.connection.rollback() #like undo anything
            raise