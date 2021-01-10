from discord.ext import commands, tasks
import random

class DefaultCog(commands.Cog):

    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def cog_unload(self):
        self.printer.cancel()

    @commands.command(pass_context = True, name="99", help='Respond a random sentence eheheh', )
    async def nine_nine(self, ctx):
    
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
    
    @commands.command(pass_context = True, name="ping", help='Ping Pong')
    async def ping(self, ctx):
        response = 'Pong !'
        await ctx.send(response)

    @commands.command(pass_context = True, name="Mood")
    async def set_reaction(self, ctx):

        await ctx.message.add_reaction('🥰') #Amoureux
        await ctx.message.add_reaction('🙂') #Bonne jounrée
        await ctx.message.add_reaction('😃') #Joyeux.se
        await ctx.message.add_reaction('😐') #Neutre
        await ctx.message.add_reaction('😕') #Déçu.e
        await ctx.message.add_reaction('😫') #Epuisé.e
        await ctx.message.add_reaction('🤬') #Colérique
        await ctx.message.add_reaction('🙁') #Mauvaise journée
        await ctx.message.add_reaction('😌') #Zen