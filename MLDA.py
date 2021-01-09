# bot.py
import os

import discord, random, aiocron, mysql.connector
from DefaultCog import *
from SchedulesCog import *
from dotenv import load_dotenv
from discord.ext import commands, tasks

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='??')
bot.add_cog(DefaultCog(bot))
bot.add_cog(SchedulesCog(bot))

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_reaction_add(reaction, user):
    print("Reaction ajouté Bro !")
    print(reaction.emoji)
    print(reaction.message.content)
    print(user.id)

##-----------------------------------------------
##-----------------------------------------------
##-----------------------------------------------
    
# True cron date 30 19 */1 * *
@aiocron.crontab('*/1 * * * *')
async def cronJob():
    #user = bot.get_user('176264765214162944')
    #await user.send('??Mood\n08.01.2021\nBonjour, comment s\'est passé ta journée ?')
    print("LOL")

bot.run(TOKEN)
