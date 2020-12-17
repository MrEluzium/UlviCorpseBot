# enable SERVER MEMBERS INTENT bot settings in the Discord developer portal
import discord
import asyncio
import sqlite3
import progressbar
from discord.ext import tasks, commands
from os import name as os_name
from datetime import datetime, timedelta
from Classes.Paginator import Paginator
from Classes.Character import CharacterControl
from Classes.Enemies import EnemyControl
from Classes.Guild import GuildControl
from Classes.Shop import ShopControl
from settings import TOKEN
Character = CharacterControl()
Guild = GuildControl()
Enemy = EnemyControl()
Armour = ShopControl('Armours')
Weapon = ShopControl('Weapons')
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)


async def set_activity(score=0):
    activities = ['#StayHome', f'on {len(bot.guilds)} servers!', 'Cake is a lie!', 'Your princess is in another castle!']
    cur_activity = discord.Game(activities[score])
    await bot.change_presence(status=discord.Status.online, activity=cur_activity)


@bot.event
async def on_ready():
    await set_activity(3)
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
    await ctx.send(f'> *Модленный режим установлен на {time} во всех каналах*')


@bot.command(name='edit_mob')
@commands.check(check_admin)
async def edit_mob(ctx):
    context = ctx.message.content.split()

    if len(context) < 4:
        await ctx.send('> *Введены не все параметры!*')
        return
    else:
        name, column, new = context[1], context[2], context[3]
        mob = Enemy.read(name)
        if mob:
            try:
                Enemy.edit(name, column, new)
                await ctx.send('> *Готово!*')
                mob = Enemy.read(context[1])
                await ctx.send(f'>>> **id:** *{mob[0]}*\n'
                               f'**name:** *{mob[1]}*\n'
                               f'**bowed_name:** *{mob[2]}*\n'
                               f'**hp:** *{mob[3]}*\n'
                               f'**power:** *{mob[4]}*\n'
                               f'**exp:** *{mob[5]}*\n'
                               f'**money:** *{mob[6]}*\n'
                               f'**icon:** *{mob[7]}*\n'
                               f'**color:** *{mob[8]}*\n')
            except sqlite3.IntegrityError as e:
                await ctx.send(f'> *{e}*')
            except sqlite3.OperationalError or sqlite3.IntegrityError as e:
                await ctx.send(f'> *{e}*')
        else:
            await ctx.send('> *Такого существа нет!*')


@bot.command(name='remove_mob', aliases=['delmob'])
@commands.check(check_admin)
async def remove_mob(ctx):
    context = ctx.message.content.split()

    if len(context) < 2:
        await ctx.send('> *Введите имя моба!*')
        return
    else:
        name = context[1]
        try:
            Enemy.remove(name)
            await ctx.send('> *Готово!*')
        except sqlite3.OperationalError as e:
            await ctx.send(f'> *{e}*')


@bot.command(name='create_mob', aliases=['makemob'])
@commands.check(check_admin)
async def create_mob(ctx):
    context = ctx.message.content.split()

    if len(context) < 7:
        await ctx.send('> *Введены не все обязательные параметры!*')
        return
    elif len(context) == 7:
        Enemy.create(context[1], context[2], context[3], context[4], context[5], context[6])
    elif len(context) == 8:
        try:
            color = int(context[7])
            Enemy.create(context[1], context[2], context[3], context[4], context[5], context[6], color=color)
        except ValueError:
            Enemy.create(context[1], context[2], context[3], context[4], context[5], context[6], icon=context[7])
    else:
        Enemy.create(context[1], context[2], context[3], context[4], context[5], context[6], context[7], int(context[8]))
    await ctx.send('> *Готово!*')
    mob = Enemy.read(context[1])
    try:
        await ctx.send(f'>>> **id:** *{mob[0]}*\n'
                       f'**name:** *{mob[1]}*\n'
                       f'**bowed_name:** *{mob[2]}*\n'
                       f'**hp:** *{mob[3]}*\n'
                       f'**power:** *{mob[4]}*\n'
                       f'**exp:** *{mob[5]}*\n'
                       f'**money:** *{mob[6]}*\n'
                       f'**icon:** *{mob[7]}*\n'
                       f'**color:** *{mob[8]}*\n')
    except sqlite3.OperationalError as e:
        await ctx.send(f'> *{e}*')


@bot.command(name='get_mob_info', aliases=['mobinfo'])
@commands.check(check_admin)
async def get_mob_info(ctx):
    context = ctx.message.content.split()

    if len(context) == 1:
        await ctx.send('> *Введите имя существа!*')
        return
    mob = Enemy.read(context[1].title())
    if mob:
        try:
            await ctx.send(f'>>> **id:** *{mob[0]}*\n'
                           f'**name:** *{mob[1]}*\n'
                           f'**bowed_name:** *{mob[2]}*\n'
                           f'**hp:** *{mob[3]}*\n'
                           f'**power:** *{mob[4]}*\n'
                           f'**exp:** *{mob[5]}*\n'
                           f'**money:** *{mob[6]}*\n'
                           f'**icon:** *{mob[7]}*\n'
                           f'**color:** *{mob[8]}*\n')
        except sqlite3.OperationalError as e:
            await ctx.send(f'> *{e}*')
    else:
        await ctx.send('> *Такого существа нет!*')


@bot.command(name='add_shop_item', aliases=['additem'])
@commands.check(check_admin)
async def add_shop_item(ctx):
    types = ['Weapon', 'Armor', 'Armour']
    context = ctx.message.content.split()

    if len(context) < 5:
        await ctx.send('> *Введены не все параметры!*')
        return
    if context[1].title() not in types:
        await ctx.send('> *Введен неверный тип предмета! (Weapon/Armour)*')
        return
    try:
        stat, price = int(context[-2]), int(context[-1])
        name = " ".join(context[2:-2])
        if context[1] == "Weapon":
            Weapon.create(name, stat, price)
            await ctx.send(f'>>> Готово!\n*name: {name}\npower: {stat}\nprice: {price}*')
        else:
            Armour.create(name, stat, price)
            await ctx.send(f'>>> Готово!\n*name: {name}\nprotection: {stat}\nprice: {price}*')
    except ValueError:
        await ctx.send('> *Неверный синтаксис команды!*')


@bot.command(name='stats')
@commands.check(check_tavern)
async def stats(ctx):
    player = Character.read(ctx.author.id)

    embed_color = ctx.author.color
    if str(embed_color) == '#000000':
        embed_color = discord.colour.Colour(16777214)

    embed = discord.Embed(color=embed_color)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.add_field(name=f"**Профиль игрока**",
                    value=ctx.author.mention, inline=False)

    health_recovery = ""
    if player[10]:
        d1 = datetime.strptime(player[10], "%Y-%m-%d %H:%M:%S.%f")
        d2 = datetime.now()
        delta = d2 - d1
        delta = delta.total_seconds()

        health_recovery = f"\n\n:clock4: Восстановление через {await get_delta(delta)}"

    embed.add_field(
        name=f"**:crown: Уровень       {player[1]} \n"
             f":star: Опыт             {player[2]} | {player[4]} \n"
             f":heart: Здоровье    {player[5]} | {player[6]}\n"
             f":crossed_swords: Сила               {player[7]}\n"
             f":coin: Монеты       {player[8]}**"
             f"{health_recovery}",
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
    embed_main.set_thumbnail(url=ctx.message.guild.get_member(rating[0][0]).avatar_url)
    embed_main.add_field(name=f":crown: {rating[0][1]}  •  :crossed_swords: {rating[0][7]}",
                         value=f"**1. {ctx.message.guild.get_member(rating[0][0]).mention}**", inline=False)

    for i in range(1, 5 if max >= 5 else max + 1):
        embed_main.add_field(name=f":crown: {rating[i][1]}  •  :crossed_swords: {rating[i][7]}",
                             value=f"{i+1}. {ctx.message.guild.get_member(rating[i][0]).mention}", inline=False)
    embeds.append(embed_main)

    embed = discord.Embed(title='Рейтинг игроков', description=" ", color=16104960)
    for player in rating[5:]:
        embed.add_field(name=f":crown: {player[1]}  •  :crossed_swords: {player[7]}",
                        value=f"{count+1}. {ctx.message.guild.get_member(player[0]).mention}", inline=False)
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
    result = Enemy.get_all_by_id()
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


@bot.command(name='fight')
@commands.check(check_adventure)
async def fight(ctx):
    context = ctx.message.content.split()
    if len(context) == 1:
        await ctx.send('> *Введите имя существа!*')
        return

    mob = Enemy.read(context[1].title())
    if mob:
        mob_name, mob_bowed_name, mob_exp, mob_power, mob_hp, mob_money, mob_icon =\
            mob[1], mob[2], mob[3], mob[4], mob[5], mob[6], mob[7]

        mob_color = int(mob[8]) if mob[8] else None
        player = Character.read(ctx.author.id)

        player_id, player_lvl, player_exp, player_full_exp, player_expmax, player_hp, player_hp_max, player_power, player_money =\
            player[0], player[1], player[2], player[3], player[4], player[5], player[6], player[7], player[8]

        file, embed = await get_fight_embed(mob_name, mob_bowed_name, mob_hp, mob_power, mob_icon, mob_color, player_hp, player_power, '...')
        message = await ctx.send(file=file, embed=embed)

        await asyncio.sleep(0.5)

        new_level = False
        winner = None
        count = 0
        battle_mob_hp = mob_hp
        battle_player_hp = player_hp
        while count < 300:
            print(battle_player_hp)
            battle_mob_hp -= player_power
            if battle_mob_hp <= 0:
                winner = 'player'
                break
            battle_player_hp -= mob_power
            if battle_player_hp <= 0:
                winner = 'mob'
                break

        if battle_player_hp < player_hp_max:
            Character.set_stat(player_id, 'battle_time', str(datetime.now()))
        if winner == 'player':
            Character.set_stat(player_id, 'hp', battle_player_hp)
            Character.set_stat(player_id, 'fullexp', player_full_exp + mob_exp)
            Character.set_stat(player_id, 'money', player_money + mob_money)

            if player_exp + mob_exp >= player_expmax:
                Character.set_stat(player_id, 'exp', 0)
                Character.set_stat(player_id, 'lvl', player_lvl+1)
                Character.set_stat(player_id, 'expmax', player_expmax*2)
                Character.set_stat(player_id, 'hpmax', player_hp_max+25)
                Character.set_stat(player_id, 'power', player_power+5)
                if battle_player_hp == player_hp_max:
                    Character.set_stat(player_id, 'hp', player_hp_max + 25)
                new_level = True
            else:
                Character.set_stat(player_id, 'exp', player_exp + mob_exp)

            if new_level:
                file, embed = await get_fight_embed(mob_name, mob_bowed_name, mob_hp, mob_power, mob_icon, mob_color,
                                                    player_hp, player_power,
                                                    f'__Вы успешно победили врага__\nВаша награда: :star:{mob_exp}  •  :coin:{mob_money}', level=True)
            else:
                file, embed = await get_fight_embed(mob_name, mob_bowed_name, mob_hp, mob_power, mob_icon, mob_color, player_hp, player_power,
                                                    f'__Вы успешно победили врага__\nВаша награда: :star:{mob_exp}  •  :coin:{mob_money}')
            await message.edit(embed=embed)

        elif winner == 'mob':
            Character.set_stat(player_id, 'hp', 0)

            file, embed = await get_fight_embed(mob_name, mob_bowed_name, mob_hp, mob_power, mob_icon, mob_color,
                                                player_hp, player_power,
                                                f'__Вы не сумели победить врага__\n:heart: Ваше здоровье на нуле\n:clock4: Время восстановления: 15 минут')
            await ctx.send(embed=embed)

    else:
        await ctx.send('> *Такого существа нет!*')


async def get_fight_embed(mob_name, mob_bowed_name, mob_hp, mob_power, mob_icon, mob_color, player_hp, player_power, text, level=None):
    file = None
    embed = discord.Embed(title=f"Начался бой с {mob_bowed_name}", description=" ", color=mob_color)\
        if mob_color else discord.Embed(title=f"Начался бой с {mob_bowed_name}", description=" ")

    if mob_icon:
        file = discord.File(f"data/pictures/{mob_icon}")
        embed.set_thumbnail(url=f"attachment://{mob_icon}")
    embed.add_field(
        name=f"{mob_name}:\n:heart: {mob_hp}  •  :crossed_swords: {mob_power}\n"
             f"Вы:\n:heart: {player_hp}  •  :crossed_swords: {player_power}\n",
        value=" ‌‌‍‍", inline=False)
    embed.add_field(
        name=f"{text}",
        value=" ‌‌‍‍", inline=False)
    if level:
        embed.add_field(
            name=f"Вы получили новый уровень!",
            value=" ‌‌‍‍", inline=False)
    return file, embed


@bot.command(name='buy')
@commands.check(check_shop)
async def buy(ctx):
    types = ['Weapon', 'Armor', 'Armour']
    context = ctx.message.content.split()
    print(context)

    if len(context) == 1:
        # TODO Сообщение о пусто запросе в магазин
        return

    if context[1].title() not in types:
        # TODO Сообщение о неправильном запросе в магазин
        return
    else:
        type = 'Weapons' if context[1].title() == 'Weapon' else 'Armours'
        controller = Weapon if context[1].title() == 'Weapon' else Armour

    item_name = ""
    for word in context[2:]:
        item_name += word + " "
    item_name = item_name.rstrip()

    print(item_name)
    item = controller.read(item_name)
    if item:
        print(item_name)

    else:
        await ctx.send('> *Такого существа нет!*')


# Проверяем, участвет ли аккаунт в игре. Если нет, то создаем новоро персонажа.
async def check_player_in_game(id):
    player = Character.read(id)
    if not player:
        Character.create(id)

    elif player[10]:
        d1 = datetime.strptime(player[10], "%Y-%m-%d %H:%M:%S.%f")
        d2 = datetime.now()
        delta = d2 - d1
        delta = delta.total_seconds()

        if delta > 900:
            Character.set_stat(player[0], 'battle_time', '')
            Character.set_stat(player[0], 'hp', player[6])


async def get_delta(time):
    delta = timedelta(seconds=(900 - time))
    delta = ':'.join(str(delta).split('.')[0].split(':')[1:])
    return delta


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