import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os

# Charger le token depuis .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------- LOAD COGS -----------------
async def load_cogs():
    await bot.load_extension("cogs.enigmes")  # exemple pour le cog énigmes
    await bot.load_extension("cogs.archives")  # cog archives (vide pour l'instant)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user} !")
    await bot.tree.sync()
    print("Slash commands synchronisées !")

# ----------------- MAIN -----------------
import asyncio
async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())
