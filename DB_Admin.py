import mysql.connector as connector
from Webscrapper import *
import mysql.connector.errors


class Database:
    def __init__(self, host, user, password, database, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port
        )
        self.cursor = self.connection.cursor()

    def execute(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()  # add this line to fetch the query results
        self.commit()
        return result

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def insert_into(self, table_name, attributes, values):
        query = f"INSERT INTO {table_name} ({attributes}) VALUES ({values});"
        return self.cursor.execute(query)

    def update(self, table, value, name):
        query = f"UPDATE {table} SET Price = %s WHERE Asset_Name = %s"
        try:
            self.cursor.execute(query, (value, name))
            self.commit()
        except mysql.connector.errors.OperationalError as e:
            print(f"Lost connection to database: {e}")
            # Reconnect to database
            self.connect()
            # Retry the query
            self.cursor.execute(query, (value, name))
            self.commit()

    def update_price(self):
        scrapping()
        for name, price in info.items():
            self.update('Price', price, name)
        self.commit()








