from discord.ext import commands, tasks
from discord import Embed
import datetime, mysql.connector

# Il faut lancer la commande 'loaduser' au démarage du bot pour charger les utilisateurs de la base de données.
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
	HOUR = 21
	REGISTER = []
	REGISTER_ID = []
	FIRSTLOOP = False

	def __init__(self, bot, db):
		self.bot = bot
		self.db = db
		self.dbCursor = db.cursor()
		self.refaced()
		self.loaduser()

	def loaduser(self):
		sql = "SELECT * FROM users"
		self.dbCursor.execute(sql)

		SchedulesCog.REGISTER_ID.clear()

		SchedulesCog.REGISTER = self.dbCursor.fetchall()
		for user in SchedulesCog.REGISTER:
			SchedulesCog.REGISTER_ID.append(int(user[0]))

		print((str(len(SchedulesCog.REGISTER)) + " users load"))

	def cog_unload(self):
		self.printer.cancel()

	@tasks.loop(seconds=5.0)
	async def printer(self):
		if SchedulesCog.FIRSTLOOP == False:
			await self.pomme()
		else:
			SchedulesCog.FIRSTLOOP = False

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
				user_discord = await self.bot.fetch_user(int(user[0]))

				if user_discord:
					message = await user_discord.send(embed=embed)
					SchedulesCog.BUFFER.append(message.id)
					await self.set_reaction(message)
			self.printer.change_interval(hours=24)
		print(SchedulesCog.BUFFER)

	@commands.command()
	async def askme(self, ctx):
		
		# ADD users to my bdd 
		if ctx.author.id in SchedulesCog.REGISTER_ID and SchedulesCog.REGISTER[SchedulesCog.REGISTER_ID.index(ctx.author.id)][2] != 1:
			await ctx.send("Je te met à jour frero")
			sql = f"UPDATE Users SET mood_Sub = 1 WHERE id_Discord = {ctx.author.id}"
			self.dbCursor.execute(sql)
			self.db.commit()
		elif ctx.author.id in SchedulesCog.REGISTER_ID:
			await ctx.send("Tu es déjà ajouté fréro")
		else:
			await ctx.send("Je t'ajoute à ma liste frero")
			sql = "INSERT INTO Users (id_Discord, birthday_Sub, mood_Sub) VALUES (%s, %s, %s)"
			val = (str(ctx.author.id), 0, 1)
			self.dbCursor.execute(sql, val)
			self.db.commit()
			SchedulesCog.REGISTER_ID.append(ctx.author.id)
			SchedulesCog.REGISTER.append((str(ctx.author.id), 0, 1))
		print(self.dbCursor.rowcount, "record(s) affected") 

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		print("Hello")
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