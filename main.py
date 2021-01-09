import os
import discord

from bin.MNNITBot import MNNITBot

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = MNNITBot(intents=intents, file="data/students.json")
bot.run(TOKEN)
