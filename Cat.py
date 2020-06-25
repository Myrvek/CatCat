import discord 
from discord.ext import commands 
import datetime
import nekos 
import asyncio
import wikipedia
import pyowm
import os
from discord import utils
from discord.ext.commands import Bot
import urllib.parse
import re
import json
import io
import requests
import random 
import time
from Cybernator import Paginator
import COVID19Py

Bot = commands.Bot(command_prefix='Lt!') 
Bot.remove_command('help') 
def postfix(num:int, end_1:str='год', end_2:str='года', end_3:str='лет'): 
    num = num % 10 if num > 20 else num # Делим число на 10 и получаем то что осталось после деления, дальше проверка это больше чем 20 или нет, если больше то оставляем число не изменныс, а если меньше то заменяем число на остаток деления
    return end_1 if num == 1 else end_2 if 1 < num < 5 else end_3 # Тут уже просто прлверяем

@Bot.event
async def on_ready():
	print('Ну я тут')

@Bot.command()
async def help(ctx):
    embed1 = discord.Embed(title="Привет это все команды", description='Нажимай на стрелки и смотри команды')
    embed2 = discord.Embed(title="Эмоции", description='Lt!pat(Человек) Погладить \n Lt!hug (Человек) Обнять \n Lt!spal (Человек) ударить \n Lt!kiss (Человек) поцеловать')
    embed3 = discord.Embed(title="Игры", description='Lt!knb Сыграть в камень ножницы бумага \n Lt!wea (Город) Погода в городе \n Lt!wiki (запрос) Вики-Вики! \n Lt!ball (Запрос) спросить у шара \n Lt!gl (Запрос) гуглю за вас \n Lt!cat Котики! \n Lt!num_msg (Человек) посмотреть сколько у тебя сообшений' )
    embed4 = discord.Embed(title="Другое", description='Lt!ava (Человек) посмотреть аву себя или человека \n Lt!ran_ava Аниме ава \n Lt!profile Свой профиль или другое \n Lt!serverinfo Инфо о сервере \n Lt!covid (Название страны в коде из двух букв) Инфо о COVID-19 ')
    embeds = [embed1, embed2, embed3, embed4]
    message = await ctx.send(embed=embed1)
    page = Paginator(Bot, message, only=ctx.author, use_more=False, embeds=embeds)
    await page.start()

@Bot.event
async def on_ready():
    while True:
        await Bot.change_presence(activity= discord.Activity(name=' на сервер Лататы', type= discord.ActivityType.watching))
        await asyncio.sleep(10)
        await Bot.change_presence(activity= discord.Game("Команда помощи Lt!help"))
        await asyncio.sleep(10)

@Bot.command() # Декоратор команды
async def ava(ctx, member : discord.Member = None): # Название команды и аргументы
    user = ctx.message.author if member == None else member # Проверка аргуменат и переменная участника
    emb = discord.Embed( # Переменная ембеда
        title=f'Аватар пользователя {user}', # Заполняем заголовок
        description= f'[Ссылка на изображение]({user.avatar_url})', # Запонлняем описание
        color=user.color # Устанавливаем цвет
    )
    emb.set_image(url=user.avatar_url) # Устанавливаем картинку
    await ctx.send(embed=emb) # Отпрвака ембеда

@Bot.command()
async def knb(ctx):
    solutions = ['✂️', '🧱', '📄']
    winner = "**НИЧЬЯ**"
    msg = await ctx.send('Выберите ход :')
    for r in solutions:
        await msg.add_reaction(r)
    try:
        react, user = await Bot.wait_for('reaction_add', timeout= 30.0, check= lambda react, user: user == ctx.author and react.message.channel == ctx.channel and react.emoji in solutions)
    except asyncio.TimeoutError:
        await ctx.send('Время вышло')
        await msg.delete()
        await ctx.message.delete()
    else:
        p1 = solutions.index(f'{react.emoji}')
        p2 = random.randint(0, 2)
        if p1 == 0 and p2 == 1 or p1 == 1 and p2 == 2 or p1 == 2 and p2 == 0:
            winner = f"{ctx.message.author.mention} ты **Проиграл**"
        elif p1 == 1 and p2 == 0 or p1 == 2 and p2 == 1 or p1 == 0 and p2 == 2:
            winner = f"{ctx.message.author.mention} ты **Выиграл**"
        await ctx.send(    
            f"{ctx.message.author.mention} **=>** {solutions[p1]}\n"
            f"{Bot.user.mention} **=>** {solutions[p2]}\n"
            f"{winner}")
        await msg.delete()
        await ctx.message.delete()

@Bot.command() # Декоратор команды
async def ran_ava(ctx): # Название команды
    emb = discord.Embed(description= 'Вот подобраная Вам аватарка.') # Переменная ембеда и его описание
    emb.set_image(url=nekos.img('avatar')) # Тут мы с помощью новой библиотеки ищем картинку на тему аватар и ставим её в ембед
    await ctx.send(embed=emb)  # Отпрвака ембеда

@Bot.command() # Декоратор команды
async def kiss(ctx, member : discord.Member): # Название команды и аргумент
    if member == ctx.message.author: # Проверка кого упомянули
        await ctx.send('Вы не можете поцеловать сами себя.')
    else:
        emb = discord.Embed(description= f'{member.mention}, Вас поцеловал(а) {ctx.message.author.mention}.') # Переменная ембеда и описание
        emb.set_image(url=nekos.img('kiss')) # Ищем картинку и ставим её в ембед

        await ctx.send(embed=emb) # Отпрвака ембед
#work
        
@Bot.command() # Декоратор команды
async def hug(ctx, member : discord.Member): # Название команды и аргумент
    if member == ctx.message.author: # Проверка кого упомянули
        await ctx.send('Вы не можете обнять сами себя.')
    else:
        emb = discord.Embed(description= f'{member.mention}, Вас обнял(а) {ctx.message.author.mention}.') # Переменная ембеда и описание
        emb.set_image(url=nekos.img('hug')) # Ищем картинку и ставим её в ембед

        await ctx.send(embed=emb) # Отпрвака ембед
#work
        
@Bot.command() # Декоратор команды
async def slap(ctx, member : discord.Member): # Название команды и аргумент
    if member == ctx.message.author: # Проверка кого упомянули
        await ctx.send('Вы не можете ударить сами себя.')
    else:
        emb = discord.Embed(description= f'{member.mention}, Вас ударил(а) {ctx.message.author.mention}.') # Переменная ембеда и описание
        emb.set_image(url=nekos.img('slap')) # Ищем картинку и ставим её в ембед

        await ctx.send(embed=emb) # Отпрвака ембед
#work
        
@Bot.command() # Декоратор команды
async def pat(ctx, member : discord.Member): # Название команды и аргумент
    if member == ctx.message.author: # Проверка кого упомянули
        await ctx.send('Вы не можете погладить сами себя.')
    else:
        emb = discord.Embed(description= f'{member.mention}, Вас погладил(а) {ctx.message.author.mention}.') # Переменная ембеда и описание
        emb.set_image(url=nekos.img('pat')) # Ищем картинку и ставим её в ембед

        await ctx.send(embed=emb) # Отпрвака ембед

@Bot.command() # Декоратор команды
async def profile(ctx, userf: discord.Member = None): # Название команды и аргумент
    user = ctx.message.author if userf == None else userf # Проверка указан ли пользователь, если нет то заменяем автором команды
    status = user.status # Получаем статус

    if user.is_on_mobile() == True: stat = 'На телефоне' # Проверка статуса и указываем статус
    if status == discord.Status.online: stat = 'В сети' # Проверка статуса и указываем статус
    elif status == discord.Status.offline: stat = 'Не в сети' # Проверка статуса и указываем статус
    elif status == discord.Status.idle: stat = 'Не активен' # Проверка статуса и указываем статус
    elif status == discord.Status.dnd: stat = 'Не беспокоить' # Проверка статуса и указываем статус

    create_time = (datetime.datetime.today()-user.created_at).days # Узнаем кол-во дней в дискорде
    join_time = (datetime.datetime.today()-user.joined_at).days # Узнаем кол-во дней на сервере

    emb = discord.Embed(title='Профиль', colour= user.color) # Делаем ембед и устанавливаем цвет
    emb.add_field(name= 'Ник', value= user.display_name, inline= False) # Добавляем поле и заполняем 
    emb.add_field(name= 'ID', value= user.id, inline= False) # Добавляем поле и заполняем 
    
    if create_time == 0: # Проверка на число дней
        emb.add_field(name= 'Присоиденился к дискорду', value= f'{user.created_at.strftime("%d.%m.%Y")} ( Меньше дня )', inline= False) # Добавляем поле и заполняем дни в дискорде
    else:
        emb.add_field(name= 'Присоиденился к дискорду', value= f'{user.created_at.strftime("%d.%m.%Y")} ( {create_time} {postfix(create_time, "день", "дня", "дней")})', inline= False)# Добавляем поле и заполняем кол-во дней в дискорде и подбираем окончание
    if join_time == 0: # Проверка на число дней
        emb.add_field(name= 'Присоединился к серверу', value= f'{user.joined_at.strftime("%d.%m.%Y")} ( Меньше дня )', inline= False) # Добавляем поле и заполняем дни на сервере
    else:
        emb.add_field(name= 'Присоединился к серверу', value= f'{user.joined_at.strftime("%d.%m.%Y")} ( {join_time} {postfix(join_time, "день", "дня", "дней")} )', inline= False) # Добавляем поле и заполняем кол-во дней на сервере и подбираем окончание
    emb.add_field(name= 'Наивысшая роль', value= f"<@&{user.top_role.id}>", inline= False) # Добавляем поле и заполняем роль
    emb.add_field(name= 'Статус', value= stat, inline= False) # Добавляем поле и заполняем статус
    emb.set_thumbnail(url= user.avatar_url) # Устанавливаем картинку сбоку ( В душе хз как назвать xD )

    await ctx.send(embed=emb) 

owm = pyowm.OWM('9963f6627710292d5125e8200fc5b2b5', language= 'ru')
@Bot.command()
async def wea(ctx, *, arg):
    observation = owm.weather_at_place(arg)
    w = observation.get_weather()
    prs = w.get_pressure()
    tmp = w.get_temperature('celsius')
    hmd = w.get_humidity()
    cld = w.get_clouds()
    wnd = w.get_wind()
    wnds = wnd.get('speed')
    wnds_str = ''
    rn = w.get_rain()
    emb = discord.Embed(
        title= 'Текущая погода'
    )
    emb.add_field(
        name= 'Температура',
        value= f'{tmp.get("temp")}°'
    )
    emb.add_field(
        name= 'Давление',
        value= str(prs.get('press')) + 'мм рт.ст.'
    )
    emb.add_field(
        name= 'Влажность',
        value= str(hmd) + '%'
    )
    emb.add_field(
        name= 'Облачность',
        value= str(cld) + '%'
    )
    if wnds < 0.2:wnds_str = 'Штиль'
    elif wnds < 1.5: wnds_str = 'Тихий'
    elif wnds < 3.3: wnds_str = 'Лёгкий'
    elif wnds < 5.4: wnds_str = 'Слабый'
    elif wnds < 7.9: wnds_str = 'Умеренный'
    elif wnds < 10.7: wnds_str = 'Свежий'
    elif wnds < 13.8: wnds_str = 'Сильный'
    elif wnds < 17.1: wnds_str = 'Крепкий'
    elif wnds < 20.7: wnds_str = 'Очень крепкий'
    elif wnds < 24.4: wnds_str = 'Шторм'
    elif wnds < 28.4: wnds_str = 'Сильный шторм'
    elif wnds < 32.6: wnds_str = 'Жестокий шторм'
    elif wnds > 32.6: wnds_str = 'Ураган'
    emb.add_field(
        name= 'Степень ветра',
        value= wnds_str
    )
    emb.add_field(
        name= 'Скорость ветра',
        value= str(wnds) + ' м/с'
    )
    emb.set_image(url= w.get_weather_icon_url())
    await ctx.send(embed=emb)

@Bot.command()
async def wiki(ctx, *, text):
    wikipedia.set_lang("ru")
    new_page = wikipedia.page(text)
    summ = wikipedia.summary(text)
    emb = discord.Embed(
        title= new_page.title,
        description= summ
    )
    emb.set_author(name= 'Больше информации тут! Кликай!', url= new_page.url, icon_url= 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png')

    await ctx.send(embed=emb)    

@Bot.command()
async def serverinfo(ctx):
    members = ctx.guild.members
    online = len(list(filter(lambda x: x.status == discord.Status.online, members)))
    offline = len(list(filter(lambda x: x.status == discord.Status.offline, members)))
    idle = len(list(filter(lambda x: x.status == discord.Status.idle, members)))
    dnd = len(list(filter(lambda x: x.status == discord.Status.dnd, members)))
    allchannels = len(ctx.guild.channels)
    allvoice = len(ctx.guild.voice_channels)
    alltext = len(ctx.guild.text_channels)
    allroles = len(ctx.guild.roles)
    embed = discord.Embed(title=f"{ctx.guild.name}", color=0xff0000, timestamp=ctx.message.created_at)
    embed.description=(
        f":timer: Сервер создали **{ctx.guild.created_at.strftime('%A, %b %#d %Y')}**\n\n"
        f":flag_white: Регион **{ctx.guild.region}\n\nГлава сервера **{ctx.guild.owner}**\n\n"
        f":tools: Ботов на сервере: **{len([m for m in members if m.bot])}**\n\n"
        f":green_circle: Онлайн: **{online}**\n\n"
        f":black_circle: Оффлайн: **{offline}**\n\n"
        f":yellow_circle: Отошли: **{idle}**\n\n"
        f":red_circle: Не трогать: **{dnd}**\n\n"
        f":shield: Уровень верификации: **{ctx.guild.verification_level}**\n\n"
        f":musical_keyboard: Всего каналов: **{allchannels}**\n\n"
        f":loud_sound: Голосовых каналов: **{allvoice}**\n\n"
        f":keyboard: Текстовых каналов: **{alltext}**\n\n"
        f":briefcase: Всего ролей: **{allroles}**\n\n"
        f":slight_smile: Людей на сервере **{ctx.guild.member_count}\n\n"
    )

    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"ID: {ctx.guild.id}")
    embed.set_footer(text=f"ID Пользователя: {ctx.author.id}")
    await ctx.send(embed=embed)
@Bot.command()
async def ball(ctx, *, arg):

    message = ['Нет','Да','Возможно','Опредленно нет', 'Попробуй ещё раз' ,'Даже не думай!' ,'Никогда!'  ] 
    s = random.choice( message )
    await ctx.send(embed = discord.Embed(description = f'Кот кидает шар :pouting_cat: :right_facing_fist: :8ball:  \n и шар говорит ** {s}**', color=0x0c0c0c))
    return
@Bot.command()
async def gl( ctx, *, question ):

    url = 'https://google.gik-team.com/?q='
    emb = discord.Embed( title = question, description = 'Вот чего я должен все за тебя делать?',
                         colour = discord.Color.green(), url = url + str(question).replace(' ', '+') )
    
  
    

    await ctx.send( embed = emb )

@Bot.command()
async def cat(ctx):
    meow = random.randint(1, 100000)
    embed = discord.Embed(title='**Вот тебе котик**' ,colour=0x00ffff)
    embed.set_image(url = f'https://cataas.com/cat?{meow}')
    await ctx.send(embed=embed)
@Bot.command()
async def covid(ctx, code: str= None):
    covid19 = COVID19Py.COVID19()
    if not code:
        location = covid19.getLocationByCountryCode("RU")[0]
    else:
        code = code.upper()
        with open('country_codes.json') as h_file:
            c_codes = json.load(h_file)
        if not code in c_codes:
            await ctx.send('Неверный код страны.')
            return
        location = covid19.getLocationByCountryCode(code)[0]
    date = location['last_updated'].split("T")
    time = date[1].split(".")

    embed = discord.Embed(
        title = f'Случаи заболевания COVID-19, {location["country"]}:',
        description = f'''Заболевших: {location['latest']['confirmed']}\nСмертей: {location['latest']['deaths']}\n\nНаселение: {location['country_population']}\nПоследние обновление: {date[0]} {time[0]}''',
        color=0x0c0c0c
    )

    await ctx.send(embed = embed)



class Messages:

    def __init__(self, Bot):
        self.Bot = Bot

    async def number_messages(self, member):
        n_messages = 0
        for guild in self.Bot.guilds:
            for channel in guild.text_channels:
                try:
                    async for message in channel.history(limit = None):
                        if message.author == member:
                            n_messages += 1
                except (discord.Forbidden, discord.HTTPException):
                    continue
        return n_messages

@Bot.command(name = "messages")
async def num_msg(ctx, member: discord.Member = None):
    user = ctx.message.author if (member == None) else member
    number = await Messages(Bot).number_messages(user)
    embed = discord.Embed(description = f":envelope: Количество сообщений на сервере от **{user.name}** — **{number}**!", color= 0x39d0d6)
    await ctx.send(embed = embed)
    
token = os.environ.get('BOT_TOKEN')

Bot.run(str(token))
