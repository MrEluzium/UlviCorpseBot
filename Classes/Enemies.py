# Класс противников. Управляет базой данных.
import sqlite3
from discord import Embed, File
db_path = 'data/databases/Enemies.db'


class EnemyControl:
    def create(self, name, bowed_name, hp, power, exp, money, icon=None, color=None):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        if color:
            if icon:
                cursor.execute(
                    f"INSERT INTO Enemies(name, bowed_name, exp, power, hp, money, icon, color) VALUES('{name}', '{bowed_name}', {exp}, {power}, {hp}, {money}, '{icon}', {color});")
            else:
                cursor.execute(
                    f"INSERT INTO Enemies(name, bowed_name, exp, power, hp, money, color) VALUES('{name}', '{bowed_name}', {exp}, {power}, {hp}, {money}, {color});")
        else:
            if icon:
                cursor.execute(
                    f"INSERT INTO Enemies(name, bowed_name, exp, power, hp, money, icon) VALUES('{name}', '{bowed_name}', {exp}, {power}, {hp}, {money}, '{icon}');")
            else:
                cursor.execute(
                    f"INSERT INTO Enemies(name, bowed_name, exp, power, hp, money) VALUES('{name}', '{bowed_name}', {exp}, {power}, {hp}, {money});")

        conn.commit()
        conn.close()

    def read(self, name):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        result = cursor.execute(f"SELECT * FROM Enemies where name = '{name}';").fetchone()
        conn.close()
        return result

    def get_all(self):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        result = cursor.execute(f"SELECT * FROM Enemies").fetchall()
        conn.close()
        return result

    def get_all_by_id(self):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        result = cursor.execute(f"SELECT * FROM Enemies ORDER BY id;").fetchall()
        conn.close()
        return result

    def edit(self, name, column, new):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            new = int(new)
            cursor.execute(f"UPDATE Enemies SET {column} = {new} where name = '{name}';")
        except ValueError:
            cursor.execute(f"UPDATE Enemies SET {column} = '{new}' where name = '{name}';")
        conn.commit()
        conn.close()

    def remove(self, name):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM Enemies where name = '{name}';")
        conn.commit()
        conn.close()

    def get_embed(self, mob: tuple):
        name, exp, power, hp, money = mob[1], mob[3], mob[4], mob[5], mob[6]
        color = int(mob[8]) if mob[8] else None
        file = None
        embed = Embed(title=name, description=" ", color=color) if color else Embed(title=name, description=" ")

        if mob[7]:  # icon
            file = File(f"data/pictures/{mob[7]}")
            embed.set_thumbnail(url=f"attachment://{mob[7]}")
        embed.add_field(
            name=f":heart: Здоровье    {hp}\n"
                 f":crossed_swords: Сила              {power}\n"
                 f":star: Опыт             {exp} \n"
                 f":coin: Монеты       {money}",
            value=" ‌‌‍‍", inline=False)
        return file, embed
