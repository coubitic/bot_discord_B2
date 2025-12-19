import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
TOKEN = os.getenv('TOKEN')


bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")

# Chargement des cogs
initial_extensions = [
    "cogs.enigmes",
    "cogs.archives"
]

for extension in initial_extensions:
    bot.load_extension(extension)

bot.run(TOKEN)
