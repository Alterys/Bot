import sqlite3
from datetime import datetime
import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

conn = sqlite3.connect('bot.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS channels (channel_id INTEGER)''')
conn.commit()

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

TARGET_DATE = datetime(2025, 6, 21)


@bot.event
async def on_ready():
    print(f'{bot.user.name} подключен к Discord!')
    countdown.start()


@tasks.loop(hours=24)
async def countdown():
    now = datetime.now()
    delta = TARGET_DATE - now
    days = delta.days
    current_date = now.strftime('%Y-%m-%d')
    c.execute('SELECT channel_id FROM channels')
    channels = c.fetchall()
    for channel_id in channels:
        channel = bot.get_channel(channel_id[0])
        if channel:
            await channel.send(f'Сегодня {current_date}. До даты прихода Артёма осталось {days} дней!')
        else:
            print(f'Канал с ID {channel_id[0]} не найден.')


@bot.command()
async def addchannel(ctx, channel_id: int):
    c.execute('INSERT INTO channels VALUES (?)', (channel_id,))
    conn.commit()
    await ctx.send(f'Канал с ID {channel_id} добавлен в базу данных.')
    await daysleft(ctx)


@bot.command()
async def removechannel(ctx, channel_id: int):
    c.execute('DELETE FROM channels WHERE channel_id=?', (channel_id,))
    conn.commit()
    await ctx.send(f'Канал с ID {channel_id} удалён из базы данных.')


@bot.command()
async def daysleft(ctx):
    now = datetime.now()
    delta = TARGET_DATE - now
    days = delta.days
    current_date = now.strftime('%Y-%m-%d')
    await ctx.send(f'Сегодня {current_date}. До даты прихода Артёма осталось {days} дней!')

bot.run(TOKEN)
