import os, discord, random, aiocron, mysql.connector
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

bot.run(TOKEN)
