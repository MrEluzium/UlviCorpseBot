# Класс пермонажа.
import sqlite3
import asyncio


class CharacterControl:
    def create(self, id):
        conn = sqlite3.connect('data/Characters.db')
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO Characters VALUES('{id}', 1, 0, 240, 150, 150, 20, 0);")
        conn.commit()
        conn.close()

    def read(self, id):
        conn = sqlite3.connect('data/Characters.db')
        cursor = conn.cursor()
        result = cursor.execute(f"SELECT * FROM Characters where id = {id};").fetchone()
        conn.close()
        return result

    def set_stat(self, id, stat, new):
        conn = sqlite3.connect('data/Characters.db')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE Characters SET {stat} = {new} where id = {id};")
        conn.commit()
        conn.close()