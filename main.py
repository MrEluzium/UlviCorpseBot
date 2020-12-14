import discord
import asyncio
from time import sleep
import sqlite3
import progressbar
from discord import colour as dscolor
from discord.ext import tasks, commands
from os import name as os_name
from Classes.Character import CharacterControl
from settings import TOKEN
Character = CharacterControl()
bot = commands.Bot(command_prefix='/')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command(name='stats')
async def stats(ctx, stat_embed_ver=1):
    await check_player_in_game(ctx.author.id)

    current_char = Character.read(ctx.author.id)
    print(current_char)

    embed_color = ctx.author.color
    if str(embed_color) == '#000000':
        embed_color = dscolor.Colour(16777214)

    if stat_embed_ver:
        embed = discord.Embed(color=embed_color)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name=f"**Профиль игрока**", value=ctx.author.mention, inline=False)

        embed.add_field(name=":crown: **Уровень \n"
                             ":star: Опыт** \n"
                             ":heart: Здоровье \n"
                             ":crossed_swords: Сила \n"
                             ":coin: Монеты",
                        value="    ‌‌‍‍", inline=True)

        embed.add_field(name=f"**{current_char[1]} \n"
                             f"{current_char[2]} | {current_char[3]} \n"
                             f"{current_char[4]} | {current_char[5]} \n"
                             f"{current_char[6]} \n"
                             f"{current_char[7]}**",
                        value="    ‌‌‍‍", inline=True)
    else:
        embed = discord.Embed(color=embed_color)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name=f"**Профиль игрока**",
                        value=ctx.author.mention, inline=False)
        embed.add_field(
            name=":crown: **Уровень • 1 \n"
                 ":star: Опыт • 0 | 240** \n"
                 ":heart: Здоровье • 150 | 150\n"
                 ":crossed_swords: Сила • 1\n"
                 ":coin: Монеты • 5",
            value="    ‌‌‍‍", inline=False)
    await ctx.send(embed=embed)


# Проверяем, участвет ли аккаунт в игре. Если нет, то создаем новоро персонажа.
async def check_player_in_game(id):
    if not Character.read(id):
        Character.create(id)


@bot.command(name='author')
async def author(ctx):
    embed = discord.Embed(title="\n:heartpulse: Артём Eluzium :heartpulse: ", url="https://eluzium.aqulas.me/",
                          color=0xb04e5d)
    # embed.set_author(name="Author credits", url="https://eluzium.aqulas.me/")
    embed.add_field(name='Click on text above', value='luv u <3', inline=True)
    embed.set_thumbnail(
        url="https://sun9-69.userapi.com/impg/zDUbasmgtvggnwzK3l4L1X8ROTIhDxlQsag_kw/8BEPkbxDLpI.jpg?size=2000x2000&quality=96&proxy=1&sign=4d03032587f489432461109024f8bf2e&type=album")
    await ctx.send(embed=embed)


bot.run(TOKEN)