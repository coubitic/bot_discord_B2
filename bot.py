import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import asyncio

# Charger le token depuis .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Commande /commandes
@bot.tree.command(name="commandes", description="Affiche la liste des commandes du bot")
async def commandes(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📜 Commandes disponibles",
        color=discord.Color.blurple()
    )

    # Liste des commandes codée en dur
    commands_list = [
        ("/profil", "Affiche votre profil archéologique"),
        ("/enigme", "Lance une nouvelle énigme"),
        ("/reponse", "Répond à une énigme en cours"),
        ("/classement", "Affiche le top 5 des joueurs"),
        ("/classement_serveur", "Affiche le top 5 du serveur"),
        ("/anecdote", "Affiche une anecdote mythologique")
    ]

    for name, desc in commands_list:
        embed.add_field(name=f"**{name}**", value=desc, inline=False)

    await interaction.response.send_message(embed=embed)

# chargement des cogs
async def load_cogs():
    await bot.load_extension("cogs.enigmes")  # exemple pour le cog énigmes
    await bot.load_extension("cogs.archives")  # cog archives (profil)

# démarrage du bot
async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())
