# MLA_DBot
  
	Marie Louise d'Autriche Bot Discord

## Introduction

Marie Louise d'Autriche is a bot who ask your Mood every day at 7.00PM (GMT+1)
Marie Louise d'Autriche also reminds you of the birthdays of your loved ones

## Requierements

- dotenv : ```pip install -U python-dotenv```
- discord.py : ```pip install -U discord.py```
- mysql connector : ```pip install -U mysql-connector-python```

## Install it

To use this bot you must have a mysql's database.

You need a .env file with some data

- DISCORD_TOKEN=*discord_token*
- MY_SQL_PASSWORD=*user_password*
- MY_SQL_USERNAME=*user_name*
- MY_SQL_HOST=*host_name*
- MY_SQL_DATABASE=*db_name*

You need a database with a specific schema. You can import the MLA_Bot_BDD.sql in the repository.

If you are on Debian and on a server, create a service to keep your bot alive

```
[Unit]
Description=MLDA Discord Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/debian/BotDiscord/MLA_DBot
ExecStart=/home/debian/Python-3.9.1/python MLDA.py
Restart=always
User=debian

[Install]
WantedBy=multi-user.target
```

## Command for update the bot

In your terminal use this differents command if you have change your repository

- git pull
- service mla_bot stop
- systemctl daemon-reload
- service mla_bot start
- service mla_bot status

## Roadmap

- Module Mood
	- Add recap function
- Module Birthday
	- add date
	- create loop task
	- add requests sql
