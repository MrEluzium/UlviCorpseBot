# Класс гильдии. Управляет базой данных, каналами и ролями.
import sqlite3
import discord
from discord import colour, permissions
import asyncio


class GuildControl:
    async def on_join(self, guild):
        reason = 'RPG bot joined. Creating game zone.'

        admin_role = await guild.create_role(reason=reason, name='RPG manager', color=colour.Colour((10299717)))
        admin_overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            admin_role: discord.PermissionOverwrite(read_messages=True)
        }

        player_role = await guild.create_role(reason=reason, name='Traveler', color=colour.Colour((2847927)))
        player_overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            player_role: discord.PermissionOverwrite(read_messages=True),
            admin_role: discord.PermissionOverwrite(read_messages=True)
        }

        category = await guild.create_category('RPG', reason=reason, overwrites=player_overwrites)
        admin_channel = await guild.create_text_channel('Admin', category=category, reason=reason, slowmode_delay=3, overwrites=admin_overwrites)
        tavern_channel = await guild.create_text_channel('Таверна', category=category, reason=reason, slowmode_delay=3, overwrites=player_overwrites)
        shop_channel = await guild.create_text_channel('Рынок', category=category, reason=reason, slowmode_delay=3, overwrites=player_overwrites)
        adventure_channel = await guild.create_text_channel('Приключения', category=category, reason=reason, slowmode_delay=3, overwrites=player_overwrites)

        conn = sqlite3.connect('data/Guilds.db')
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO Guilds VALUES('{guild.id}', {admin_role.id}, {player_role.id}, {category.id}, {admin_channel.id}, {tavern_channel.id}, {shop_channel.id}, {adventure_channel.id});")
        conn.commit()
        conn.close()

    async def remove_all(self, guild, soft=False):
        reason = 'Removing of RPG bot was caused. Deleting game zone.'

        # Get and delete guild data from DB
        conn = sqlite3.connect('data/Guilds.db')
        cursor = conn.cursor()
        result = cursor.execute(f"SELECT * FROM Guilds where id = {guild.id};").fetchone()
        cursor.execute(f"DELETE FROM Guilds where id = {guild.id};")
        conn.commit()
        conn.close()

        [await guild.get_role(result[i]).delete(reason=reason) for i in range(1, 3)]  # Delete roles
        [await guild.get_channel(result[i]).delete(reason=reason) for i in range(7, 2, -1)]  # Delete channels amd category

        if not soft:
            await guild.leave()

    def read(self, id):
        conn = sqlite3.connect('data/Guilds.db')
        cursor = conn.cursor()
        result = cursor.execute(f"SELECT * FROM Guilds where id = {id};").fetchone()
        conn.close()
        return result

    async def set_slowmode(self, guild, time):
        conn = sqlite3.connect('data/Guilds.db')
        cursor = conn.cursor()
        result = cursor.execute(f"SELECT * FROM Guilds where id = {guild.id};").fetchone()
        conn.close()
        [await guild.get_channel(result[i]).edit(reason=f'Set RPG slowmode delay to {time}', slowmode_delay=time) for i in range(4, 8)]
