import os, discord, random, aiocron, mysql.connector
from DefaultCog import *
from SchedulesCog import *
from dotenv import load_dotenv
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
intents.reactions = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

mydb = mysql.connector.connect(
    host=os.getenv('MY_SQL_HOST'),
    user=os.getenv('MY_SQL_USERNAME'),
    password=os.getenv('MY_SQL_PASSWORD'),
    database=os.getenv('MY_SQL_DATABASE')
)

bot = commands.Bot(command_prefix='??', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!\n')
    bot.add_cog(DefaultCog(bot, mydb))
    bot.add_cog(SchedulesCog(bot, mydb))
bot.run(TOKEN)
