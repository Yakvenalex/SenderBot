import sqlite3


class Database_sql:
    def __init__(self, patch_to_db='sender.db'):
        self.patch_to_db = patch_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.patch_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def create_table_users(self):
        sql = '''
        CREATE TABLE Users (
        phone varchar(255) NOT NULL,
        link varchar(255) NOT NULL,
        status varchar(255)
        );
        '''

        self.execute(sql, commit=True)

    def create_table_pattern(self):
        sql = '''
        CREATE TABLE Pattern (
        name varchar(255) NOT NULL,
        text varchar(255) NOT NULL,
        PRIMARY KEY(name)
        );
        '''

        self.execute(sql, commit=True)

    def add_user(self, phone, link, status='send'):
        sql = 'INSERT INTO Users(phone, link, status) VALUES(?, ?, ?)'
        parameters = (phone, link, status)
        self.execute(sql, parameters=parameters, commit=True)

    def add_pattern(self, name, text):
        sql = 'INSERT INTO Pattern(name, text) VALUES(?, ?)'
        parameters = (name, text)
        self.execute(sql, parameters=parameters, commit=True)

    def select_all_users(self):
        sql = "SELECT * FROM Users"
        return self.execute(sql, fetchall=True)

    def select_all_pattern(self):
        sql = "SELECT * FROM Pattern"
        return self.execute(sql, fetchall=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f'{item} = ?' for item in parameters.keys()
        ])
        return sql, tuple(parameters.values())

    def select_pattern(self, **kwargs):
        sql = "SELECT * FROM Pattern WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def count_users(self):
        return self.execute('SELECT COUNT(*) FROM Users;', fetchone=True)

    def count_pattern(self):
        return self.execute('SELECT COUNT(*) FROM Pattern;', fetchone=True)

    def update_text(self, text, name):
        sql = 'UPDATE Pattern SET text=? WHERE name=?'
        return self.execute(sql, parameters=(text, name), commit=True)

    def delete_all_users(self):
        self.execute('DELETE FROM Users WHERE True', commit=True)

    def delete_all_pattern(self):
        self.execute('DELETE FROM Pattern WHERE True', commit=True)

def logger(statement):
    print(f'Сделал {statement}')
