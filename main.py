import os
import discord
from dotenv import load_dotenv

from bin.MNNITBot import MNNITBot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = MNNITBot(intents=intents, file="data/students.json")
bot.run(TOKEN)
