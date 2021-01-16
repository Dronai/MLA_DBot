from discord.ext import commands, tasks
import random

class DefaultCog(commands.Cog):

    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def cog_unload(self):
        self.printer.cancel()

    @commands.command(pass_context = True)
    async def ping(self, ctx):
        response = 'Pong !'
        await ctx.send(response)

    @commands.command(pass_context = True)
    async def ping_db(self, ctx):
        print("Database connected : " + str(self.db.is_connected()))
        await ctx.message.reply("Database connected : " + str(self.db.is_connected()))