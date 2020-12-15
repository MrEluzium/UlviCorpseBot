# Класс противников. Управляет базой данных.
import sqlite3
from discord import Embed, File
db_path = 'data/databases/Enemies.db'


class EnemyControl:
    def create(self, name, hp, power, exp, money, icon=None):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        if icon:
            cursor.execute(f"INSERT INTO Enemies(name, hp, power, exp, money, icon) VALUES('{name}', {hp}, {power}, {exp}, {money}, '{icon}');")
        else:
            cursor.execute(f"INSERT INTO Enemies(name, hp, power, exp, money) VALUES('{name}', {hp}, {power}, {exp}, {money});")
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

    def edit(self, name, column, new):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"UPDATE Enemies SET {column} = {new} where name = '{name}';")
        conn.commit()
        conn.close()

    def get_embed(self, mob: tuple):
        name, hp, power, exp, money, icon, color = mob[1], mob[2], mob[3], mob[4], mob[5], mob[6], int(mob[7])
        file = None
        embed = Embed(title=name, description=" ", color=color) if color else Embed(title=name, description=" ")

        if icon:
            file = File(f"data/pictures/{icon}")
            embed.set_thumbnail(url=f"attachment://{icon}")
        embed.add_field(
            name=f":heart: Здоровье    {hp}\n"
                 f":crossed_swords: Сила              {power}\n"
                 f":star: Опыт             {exp} \n"
                 f":coin: Монеты       {money}",
            value=" ‌‌‍‍", inline=False)
        return file, embed
