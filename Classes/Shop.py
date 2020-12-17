# Класс магазина. Управляет базой данных.
import sqlite3
import uuid
db_path = 'data/databases/Shop.db'


class ShopControl:
    def __init__(self, type: str = 'Weapons' or 'Armours'):
        self.type = type

    def create(self, name, stat, price):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {self.type} VALUES('{uuid.uuid4()}', '{name}', {stat}, {price});")
        conn.commit()
        conn.close()

    def read(self, name):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        result = cursor.execute(f"SELECT * FROM {self.type} where name = '{name}';").fetchone()
        conn.close()
        return result

    def set_stat(self, name, column, new):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"UPDATE {self.type} SET {column} = {new} where name = '{name}';")
        conn.commit()
        conn.close()