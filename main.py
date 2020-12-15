import discord
import asyncio
import sqlite3
import progressbar
from discord import colour as dscolor
from discord.ext import tasks, commands
from os import name as os_name
from Classes.Paginator import Paginator
from Classes.Character import CharacterControl
from Classes.Guild import GuildControl
from Classes.Enemies import EnemyControl
from settings import TOKEN
Character = CharacterControl()
Guild = GuildControl()
Enemy = EnemyControl()
bot = commands.Bot(command_prefix='/')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_guild_join(guild):
    print(f'\nJoined {guild.name}\n'
          f'ID: {guild.id}\n'
          f'Region: {guild.region}\n'
          f'Amount: {len(guild.members)}')

    await Guild.on_join(guild)


def check_admin(ctx):
    result = Guild.read(ctx.guild.id)
    if ctx.channel.id == result[4]:
        for i in ctx.message.author.roles:
            if i.id == result[1]:
                return True
    return False


async def check_tavern(ctx):
    await check_player_in_game(ctx.author.id)
    result = Guild.read(ctx.guild.id)
    if ctx.channel.id == result[5]:
        return True
    return False


async def check_shop(ctx):
    await check_player_in_game(ctx.author.id)
    result = Guild.read(ctx.guild.id)
    if ctx.channel.id == result[6]:
        return True
    return False


async def check_adventure(ctx):
    await check_player_in_game(ctx.author.id)
    result = Guild.read(ctx.guild.id)
    if ctx.channel.id == result[7]:
        return True
    return False


@bot.command(name='guild_deploy', aliases=['glddep'])
async def guild_deploy(ctx):
    if Guild.read(ctx.guild.id) is None:
        await on_guild_join(ctx.guild)


@bot.command(name='guild_remove', aliases=['gldrem'])
@commands.check(check_admin)
async def guild_remove(ctx):
    await Guild.remove_all(ctx.guild)


@bot.command(name='guild_remove_soft', aliases=['gldrems'])
@commands.check(check_admin)
async def guild_remove(ctx):
    await Guild.remove_all(ctx.guild, soft=True)


@bot.command(name='set_slowmode', aliases=['setslow'])
@commands.check(check_admin)
async def set_slowmode(ctx, time):
    await Guild.set_slowmode(ctx.guild, time)


@bot.command(name='edit_mob')
@commands.check(check_admin)
async def edit_mob(ctx):
    data = ctx.message.content[9:].split()
    name, column, new = data[0], data[1], data[2]
    mob = Enemy.read(name)
    if mob:
        try:
            Enemy.edit(name, column, new)
        except sqlite3.OperationalError as e:
            await ctx.send(f'> *{e}*')
    else:
        await ctx.send('> *Такого существа нет!*')


@bot.command(name='get_mob_info', aliases=['mobinfo'])
@commands.check(check_admin)
async def get_mob_info(ctx):
    command_len = 14 if 'get_mob_info' in ctx.message.content else 9
    if len(ctx.message.content) < command_len:
        await ctx.send('> *Введите имя существа!*')
        return
    mob = Enemy.read(ctx.message.content[command_len:].title())
    if mob:
        try:
            await ctx.send(f'>>> **id:** *{mob[0]}*\n'
                           f'**name:** *{mob[1]}*\n'
                           f'**hp:** *{mob[2]}*\n'
                           f'**power:** *{mob[3]}*\n'
                           f'**exp:** *{mob[4]}*\n'
                           f'**money:** *{mob[5]}*\n'
                           f'**icon:** *{mob[6]}*\n'
                           f'**color:** *{mob[7]}*\n')
        except sqlite3.OperationalError as e:
            await ctx.send(f'> *{e}*')
    else:
        await ctx.send('> *Такого существа нет!*')



@bot.command(name='stats')
@commands.check(check_tavern)
async def stats(ctx, stat_embed_ver=2):
    current_char = Character.read(ctx.author.id)

    embed_color = ctx.author.color
    if str(embed_color) == '#000000':
        embed_color = dscolor.Colour(16777214)

    if stat_embed_ver == 0:
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

    elif stat_embed_ver == 1:
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

    elif stat_embed_ver == 2:
        embed = discord.Embed(color=embed_color)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name=f"**Профиль игрока**",
                        value=ctx.author.mention, inline=False)
        embed.add_field(
            name="**:crown: Уровень       1 \n"
                 ":star: Опыт             0 | 240 \n"
                 ":heart: Здоровье    150 | 150\n"
                 ":crossed_swords: Сила               1\n"
                 ":coin: Монеты       10**",
            value=" ‌‌‍‍", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='top')
@commands.check(check_tavern)
async def top(ctx):
    count = 5
    rating = Character.get_by_exp()
    max = len(rating) - 1
    embeds = list()

    embed_main = discord.Embed(title='Рейтинг игроков', description=" ", color=16104960)
    embed_main.set_thumbnail(url=bot.get_user(rating[0][0]).avatar_url)
    embed_main.add_field(name=f":star:{rating[0][3]}  •  :crossed_swords: {rating[0][7]}",
                    value=f"**1. {bot.get_user(rating[0][0]).mention}**", inline=False)

    for i in range(1, 5 if max >= 5 else max + 1):
        embed_main.add_field(name=f":star:{rating[i][3]}  •  :crossed_swords: {rating[i][7]}",
                        value=f"{i+1}. {bot.get_user(rating[i][0]).mention}", inline=False)
    embeds.append(embed_main)

    embed = discord.Embed(title='Рейтинг игроков', description=" ", color=16104960)
    for player in rating[5:]:
        embed.add_field(name=f":star:{player[3]}  •  :crossed_swords: {player[7]}",
                        value=f"{count+1}. {bot.get_user(player[0]).mention}", inline=False)
        if count == max:
            embeds.append(embed)
            break
        if (count + 1) % 5 == 0:
            embeds.append(embed)
            embed = discord.Embed(title='Рейтинг игроков', description=" ", color=16104960)
        count += 1

    message = await ctx.send(embed=embed_main)
    page = Paginator(bot, message, use_more=False, embeds=embeds)
    await page.start()


@bot.command(name='moblist', aliases=['mobs'])
@commands.check(check_adventure)
async def moblist(ctx):
    result = Enemy.get_all()
    names_list = list()
    [names_list.append(mob[1]) for mob in result]

    embed = discord.Embed(title='Доступные существа', description=" ", color=4631782)
    embed_text = ""
    for mob in names_list:
        embed_text += f":diamond_shape_with_a_dot_inside: {mob}\n"
    embed_text += "\n"
    embed.add_field(
        name=embed_text, value="Ипользуй /mob [имя]‌‌‍‍", inline=False)

    await ctx.send(embed=embed)


@bot.command(name='mob')
@commands.check(check_adventure)
async def mob(ctx):
    if len(ctx.message.content) < 5:
        await ctx.send('> *Введите имя существа!*')
        return
    mob = Enemy.read(ctx.message.content[5:].title())
    if mob:
        file, embed = Enemy.get_embed(mob)
        await ctx.send(file=file, embed=embed)
    else:
        await ctx.send('> *Такого существа нет!*')


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
    file = discord.File("data/pictures/Author.jpg")
    embed.set_thumbnail(url="attachment://Author.jpg")
    await ctx.send(file=file, embed=embed)


bot.run(TOKEN)