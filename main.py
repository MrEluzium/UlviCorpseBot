import discord
import asyncio
import sqlite3
import progressbar
from discord import colour as dscolor
from discord.ext import tasks, commands
from os import name as os_name
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


@bot.command(name='moblist', aliases=['mobs'])
@commands.check(check_adventure)
async def moblist(ctx):
    result = Enemy.get_all()
    embed_list = list()
    file_list = list()
    for mob in result:
        file, embed = Enemy.get_embed(mob)
        embed_list.append(embed)
        file_list.append(file)
    print(file_list, embed_list)
    mes = await ctx.send(file=file, embed=embed)
    # page = Paginator(bot, mes, use_more=False, embeds=embed_list, use_images=True, images=file_list)
    # await page.start()


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


@bot.command(name='top')
@commands.check(check_tavern)
async def top(ctx):
    # TODO top
    pass


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