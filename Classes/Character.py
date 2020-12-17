# Класс пермонажа. Управляет базой данных.
import sqlite3
db_path = 'data/databases/Characters.db'


class CharacterControl:
    def create(self, id):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO Characters(id, lvl, exp, fullexp, expmax, hp, hpmax, power, money) VALUES('{id}', 1, 0, 0, 240, 50, 50, 1, 0);")
        conn.commit()
        conn.close()

    def read(self, id):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        result = cursor.execute(f"SELECT * FROM Characters where id = {id};").fetchone()
        conn.close()
        return result

    def set_stat(self, id, stat, new):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            new = int(new)
            cursor.execute(f"UPDATE Characters SET {stat} = {new} where id = {id};")
        except ValueError:
            cursor.execute(f"UPDATE Characters SET {stat} = '{new}' where id = {id};")
        conn.commit()
        conn.close()

    def get_by_exp(self):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        result = cursor.execute(f"SELECT * FROM Characters ORDER BY fullexp DESC;").fetchall()
        conn.close()
        return result