import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import random

"""
Cog Archives
Contient les commandes : /profil et /anecdote
Gère l'affichage du profil archéologique et des anecdotes mythologiques
"""

# Fichier JSON des utilisateurs
USERS_FILE = "data/users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

class Archives(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ----------------- /profil -----------------
    @app_commands.command(
        name="profil",
        description="Affiche votre profil archéologique"
    )
    async def profil(self, interaction: discord.Interaction):
        users = load_users()
        user_id = str(interaction.user.id)
        # vérifie le cas où le joueur n'a pas encore résolu d'énigmes
        if user_id not in users:
            await interaction.response.send_message(
                "📜 Votre profil est vide pour le moment.\n"
                "Résolvez une énigme pour commencer votre journal archéologique.",
                ephemeral=True
            )
            return

        user = users[user_id]

        enigmes_resolues = len(user.get("enigmes_resolues", []))
        score = user.get("score", 0)

        # Détermination du titre selon le score
        if score >= 20:
            titre = "🏛️ Conservateur des mythes"
            color = discord.Color.purple()
        elif score >= 10:
            titre = "🗿 Archéologue"
            color = discord.Color.gold()
        elif score >= 5:
            titre = "🧭 Explorateur"
            color = discord.Color.blue()
        else:
            titre = "📖 Novice"
            color = discord.Color.light_grey()

        # création de l'embed et de chaque fields
        embed = discord.Embed(
            title=f"📜 Profil de {interaction.user.name}",
            color=color
        )

        embed.add_field(
            name="🧩 Énigmes découvertes",
            value=str(enigmes_resolues),
            inline=True
        )
        embed.add_field(
            name="⭐ Score total",
            value=str(score),
            inline=True
        )
        embed.add_field(
            name="🏷️ Statut archéologique",
            value=titre,
            inline=False
        )

        embed.set_footer(text="Votre profil conserve la mémoire de vos découvertes.")

        await interaction.response.send_message(embed=embed)

    # Commande /anecdote : renvoie une anecdote mythologique aléatoire
    @app_commands.command(
        name="anecdote",
        description="Donne une anecdote aléatoire sur la mythologie"
    )
    async def anecdote(self, interaction: discord.Interaction):
        anecdotes = [
            "Le Minotaure vivait dans un labyrinthe conçu par Dédale à Crète.",
            "La guerre de Troie a été déclenchée par l'enlèvement d'Hélène.",
            "Hermès, dieu messager, portait des sandales ailées.",
            "Le roi Midas avait le pouvoir de transformer tout ce qu'il touchait en or.",
            "Prométhée a volé le feu aux dieux pour le donner aux hommes.",
            "Le phénix renaît de ses cendres tous les 500 ans.",
            "Achille était invincible sauf sur son talon.",
            "L'anneau de Gyges rend invisible celui qui le porte."
        ]

        # sélection d'une anecdote aléatoirement
        anecdote = random.choice(anecdotes)

        embed = discord.Embed(
            title="📜 Anecdote mythologique",
            description=anecdote,
            color=discord.Color.gold()
        )

        embed.set_footer(text="Apprenez et explorez le monde des mythes !")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Archives(bot))
