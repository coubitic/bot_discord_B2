import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} commandes slash synchronisées")
    except Exception as e:
        print(e)

# charger les cogs correctement (async)
async def load_cogs():
    for ext in ["cogs.enigmes", "cogs.archives"]:
        await bot.load_extension(ext)

asyncio.run(load_cogs())

bot.run(TOKEN)
