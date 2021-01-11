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
	HOUR = 19
	REGISTER = []
	REGISTER_ID = []

	def __init__(self, bot, db):
		self.bot = bot
		self.db = db
		self.firstloop = True
		self.dbCursor = db.cursor()
		self.refaced()
		self.loaduser()

	def loaduser(self):
		sql = "SELECT * FROM users"
		self.dbCursor.execute(sql)

		SchedulesCog.REGISTER_ID.clear()

		for user in self.dbCursor.fetchall():
			SchedulesCog.REGISTER.append([int(user[0]), user[1], user[2]])
			SchedulesCog.REGISTER_ID.append(int(user[0]))

		print((str(len(SchedulesCog.REGISTER)) + " users load"))

	def cog_unload(self):
		self.printer.cancel()

	@tasks.loop(seconds=5.0)
	async def printer(self):
		if self.firstloop == False:
			await self.askme()
		else:
			self.firstloop = False

	async def askme(self, ctx=None):
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
				if user[2] == 1:
					user_discord = await self.bot.fetch_user(user[0])

					if user_discord:
						message = await user_discord.send(embed=embed)
						SchedulesCog.BUFFER.append(message.id)
						await self.set_reaction(message)

			self.printer.change_interval(hours=24)

	@commands.command(help="Vous inscrit au processus")
	async def submood(self, ctx):
		
		# ADD users to my bdd 
		if ctx.author.id in SchedulesCog.REGISTER_ID and SchedulesCog.REGISTER[SchedulesCog.REGISTER_ID.index(ctx.author.id)][2] != 1:
			await ctx.send("*Je te connais toi non ?*\nTu viens de t'inscire à la demande de Mood.\n Cette question te sera posée tous les jours à 19h00 (GMT+1)")
			sql = f"UPDATE users SET mood_Sub = 1 WHERE id_Discord = {ctx.author.id}"
			self.dbCursor.execute(sql)
			self.db.commit()
			SchedulesCog.REGISTER[SchedulesCog.REGISTER_ID.index(ctx.author.id)][2] = 1
			print(self.dbCursor.rowcount, "record(s) affected")
		elif ctx.author.id in SchedulesCog.REGISTER_ID:
			await ctx.send("Tu es déjà inscit à la demande de Mood quotidienne.")
		else:
			await ctx.send("*On ne se connais pas encore il me semble* ?\nTu viens de t'inscire à la demande de Mood.\n Cette question te sera posée tous les jours à 19h30 (GMT+1)")
			sql = "INSERT INTO users (id_Discord, birthday_Sub, mood_Sub) VALUES (%s, %s, %s);"
			val = (str(ctx.author.id), 0, 1)
			self.dbCursor.execute(sql, val)
			self.db.commit()
			SchedulesCog.REGISTER_ID.append(ctx.author.id)
			SchedulesCog.REGISTER.append([str(ctx.author.id), 0, 1])
			print(self.dbCursor.rowcount, "record(s) affected")
	
	@commands.command(help="Vous désinscrit du processus")
	async def unsubmood(self, ctx):
		if ctx.author.id in SchedulesCog.REGISTER_ID and SchedulesCog.REGISTER[SchedulesCog.REGISTER_ID.index(ctx.author.id)][2] == 1:
			sql = f"UPDATE users SET mood_Sub = 0 WHERE id_Discord = {ctx.author.id}"
			self.dbCursor.execute(sql)
			self.db.commit()
			SchedulesCog.REGISTER[SchedulesCog.REGISTER_ID.index(ctx.author.id)][2] = 0
			print(self.dbCursor.rowcount, "record(s) affected")

			ctx.message.reply(f"Vous venez de vous désinscrire du processus de Mood :sad:\n Vous pouvez toujours vous réinscrire avec la commande {self.bot.command_prefix}submood !")
	
	def check_emoji(self, em):

		if em == '🥰':
			return "Amoureux"
		elif em == '🙂':
			return "Bonne journée"
		elif em == '😃':
			return "Joyeux.se"
		elif em == '😐':
			return "Neutre"
		elif em == '😕':
			return "Déçu.e"
		elif em == '😫':
			return "Epuisé.e"
		elif em == '🤬':
			return "Colérique"
		elif em == '🙁':
			return "Mauvaise journée"
		elif em == '😌':
			return "Zen"

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		if reaction.message.id in SchedulesCog.BUFFER and not user.bot and user.id in SchedulesCog.REGISTER_ID:
			emoji = reaction.emoji
			await reaction.message.reply("Ton mood a était prise en compte. Merci !")

			# Stocker le mood de la personne
			date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			emoj = self.check_emoji(emoji)
			sql = "INSERT INTO mood VALUES (%s, %s, %s);"
			val = (user.id, emoj, date)
			self.dbCursor.execute(sql, val)
			self.db.commit()
			print(self.dbCursor.rowcount, "record(s) affected")
			
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

	@commands.command(pass_context = True, help="va vous donner les commandes concernant le processus de Mood !")
	async def moodinfo(self, ctx):
		await ctx.message.reply("L'expérience Mood a pour but de vous demander votre état sur la journée à 19h00 (GMT+1)\n"
		+ "```md\n"
		+ "#Commandes Mood\n"
		+ f"- submood : Vous inscrit au processus\n"
		+ f"- unsubmood : Vous désinscrit du processus\n"
		+ f"- moodinfo : Montre ce message"
		+ f"- rgpd : Donne des informations sur la rgpd"
		+ "\n#Commandes à venir\n"
		+ f"- recap : Vous donne un récapitulatif de votre mood. (La façon de transmettre le récap n\'est pas encore déterminé\n"
		+ "```")
		
	@commands.command(help="La RGPD c'est quoi ?")
	async def rgpd(self, ctx):
		await ctx.message.reply("Hum... RGPD, c'est à propos de vos données. Des infos ici https://www.cnil.fr/fr/comprendre-le-rgpd\n\n Comment dire que vous données avec moi, Marie-Louise d'Autriche, elles sont stockées dans mon coffre et je ne les vends pas. Il y a surement moyen que je fasse des stats ou d'autres truc un jour avec mais jamais je ne ferais d'argent avec. Don\'t worry\n Si vous voulez tout de même supprimer vos données, faite signe à Dronai#2906 et il fera le nécessaire !")
