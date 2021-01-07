# bot.py
import os

import discord, random, aiocron
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='??')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name="99", help='Respond a random sentence eheheh')
async def nine_nine(ctx):
    
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        '99!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)
    
@bot.command(name="ping", help='Ping Pong')
async def ping(ctx):
    response = 'Pong !'

    await ctx.send(response)

# True cron date 30 19 */1 * *
@aiocron.crontab('* * * * *')
async def cronJob():
    print("Pomme")


bot.run(TOKEN)
