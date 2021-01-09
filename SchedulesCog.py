from discord.ext import commands, tasks
from discord import Embed
import datetime

class SchedulesCog(commands.Cog):

	REACTION = {
			"Amoureux":         "🥰",
			"Bonne journée":    "🙂",
			"Joyeux.se":        "😃",
			"Neutre":           "😐",
			"Déçu.e":           "😕",
			"Epuisé.e":         "😫",
			"Colérique":        "🤬",
			"Mauvaise journée": "🙁",
			"Zen":              "😌"
		}

	BUFFER = []
	HOUR = 16
	REGISTER = []

	def __init__(self, bot):
		self.index = 0
		self.bot = bot
		self.refaced()

	def cog_unload(self):
		self.printer.cancel()

	@tasks.loop(seconds=5.0)
	async def printer(self):
		await self.pomme()

	@commands.command()
	async def pomme(self, ctx=None):
		_ctx = None or ctx
		embed = Embed(title="How are you ?", color=0xe80005, timestamp=datetime.datetime.today())
		for mood, emoji in SchedulesCog.REACTION.items():
			embed.add_field(name=mood, value=emoji, inline=True)
		#TODO : Check if register match bdd users and get it if doesn't match
		if _ctx:
			message = await _ctx.send(embed=embed)
			SchedulesCog.BUFFER.append(message.id)
			await self.set_reaction(message)
		else:	
			for user in SchedulesCog.REGISTER:
				message = await user.send(embed=embed)
				SchedulesCog.BUFFER.append(message.id)
				self.set_reaction(message)
			self.printer.change_interval(hours=24)

	@commands.command()
	async def askme(self, ctx):
		await ctx.send("Je t'ajoute à ma liste frero")
		SchedulesCog.REGISTER.append(ctx.author)
		#TODO : ADD users to my bdd 

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		if reaction.message.id in SchedulesCog.BUFFER and not user.bot:
			emoji = reaction.emoji
			await reaction.message.reply("ça fait plaiz poto")
			# TODO: Stocker le mood de la persoone
			await reaction.message.delete()

	def refaced(self):
		hour = SchedulesCog.HOUR
		
		next_call = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
		next_call = next_call.replace(hour=hour, minute=0, second=0)
		delta = self.time_until(next_call)  

		try:
			# Change interval will only take action at the next loop
			self.printer.change_interval(seconds=delta)
			self.printer.start()
		except Exception as e:
			print(e)

	def time_until(self, when) -> float:
		if when.tzinfo is None:
			when = when.replace(tzinfo=datetime.timezone.utc)
		now = datetime.datetime.now(datetime.timezone.utc)
		delta = (when - now).total_seconds()
		return delta

	async def set_reaction(self, message):
		for emoji in SchedulesCog.REACTION.values():
			await message.add_reaction(emoji)