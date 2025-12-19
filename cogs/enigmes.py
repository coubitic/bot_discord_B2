import discord
from discord.ext import commands
from discord import app_commands
import random
import json
import os

"""
Cog Enigmes
Contient les commandes : /enigme (et /reponse), /classement et /classement_serveur
Gère le système d'énigmes et de classements
"""

# Fichiers JSON
USERS_FILE = "data/users.json"
ENIGMES_FILE = "data/enigmes.json"

def load_json(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# fonction permettant de mettre à jour les données du fichier json
def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

class Enigmes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.enigmes_en_cours = {}
        self.enigmes = load_json(ENIGMES_FILE)
        self.users = load_json(USERS_FILE)

    @app_commands.command(name="enigme", description="Pose une énigme mythologique")
    async def enigme(self, interaction: discord.Interaction):
        enigme = random.choice(self.enigmes)
        user_id = str(interaction.user.id)
        guild_id = str(interaction.guild.id)
        self.enigmes_en_cours[user_id] = enigme

        if user_id not in self.users:
            # ajoute les données de l'utilisateur dans users.json si il n'a jamais
            # fait d'énigmes avant
            self.users[user_id] = {
                "pseudo": interaction.user.name,
                "enigmes_resolues": [],
                "score": 0,
                "guilds": [guild_id]
            }
        else:
            # Ajouter le serveur courant si pas déjà présent
            if "guilds" not in self.users[user_id]:
                self.users[user_id]["guilds"] = []
            if guild_id not in self.users[user_id]["guilds"]:
                self.users[user_id]["guilds"].append(guild_id)

        save_json(USERS_FILE, self.users)

        # création de l'embed qui présente la question
        embed = discord.Embed(
            title="🧩 Nouvelle énigme !",
            description=enigme["question"],
            color=discord.Color.blue()
        )
        embed.set_footer(text="Répondez avec /reponse <votre réponse>")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="reponse", description="Répond à l'énigme en cours")
    async def reponse(self, interaction: discord.Interaction, reponse: str):
        user_id = str(interaction.user.id)
        guild_id = str(interaction.guild.id)
        if user_id not in self.enigmes_en_cours:
            await interaction.response.send_message("❌ Vous n'avez pas d'énigme en cours.")
            return

        enigme = self.enigmes_en_cours[user_id]

        if reponse.lower() == enigme["reponse"].lower():
            await interaction.response.send_message("✅ Bonne réponse !")

            if user_id not in self.users:
                self.users[user_id] = {
                    "pseudo": interaction.user.name,
                    "enigmes_resolues": [],
                    "score": 0,
                    "guilds": [guild_id]
                }
            else:
                # Ajouter le serveur courant si pas déjà présent
                if "guilds" not in self.users[user_id]:
                    self.users[user_id]["guilds"] = []
                if guild_id not in self.users[user_id]["guilds"]:
                    self.users[user_id]["guilds"].append(guild_id)

            self.users[user_id]["score"] += 1
            if enigme["id"] not in self.users[user_id]["enigmes_resolues"]:
                self.users[user_id]["enigmes_resolues"].append(enigme["id"])
            save_json(USERS_FILE, self.users)

            del self.enigmes_en_cours[user_id]
        else:
            await interaction.response.send_message(f"❌ Mauvaise réponse. Indice : {enigme['indice']}")

    @app_commands.command(name="classement", description="Affiche le top 5 des joueurs (global)")
    async def classement(self, interaction: discord.Interaction):
        if not self.users:
            await interaction.response.send_message("Aucun joueur avec un score trouvé.")
            return

        top5 = sorted(self.users.items(), key=lambda x: x[1]["score"], reverse=True)[:5]

        embed = discord.Embed(
            title="🏆 Top 5 des joueurs",
            color=discord.Color.gold()
        )

        description = ""
        medals = ["🥇", "🥈", "🥉"]
        for i, (user_id, data) in enumerate(top5, start=1):
            medal = medals[i-1] if i <= 3 else f"{i}."
            description += f"{medal} {data['pseudo']} ({data['score']} pts)\n"

        embed.description = description
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="classement_serveur", description="Affiche le top 5 des joueurs du serveur actuel")
    async def classement_serveur(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)
        # Filtrer tous les utilisateurs qui ont ce serveur dans leur liste
        guild_users = {uid: data for uid, data in self.users.items() if guild_id in data.get("guilds", [])}

        if not guild_users:
            await interaction.response.send_message("Aucun joueur avec un score trouvé sur ce serveur.")
            return

        top5 = sorted(guild_users.items(), key=lambda x: x[1]["score"], reverse=True)[:5]

        embed = discord.Embed(
            title=f"🏆 Top 5 du serveur {interaction.guild.name}",
            color=discord.Color.gold()
        )

        description = ""
        medals = ["🥇", "🥈", "🥉"]
        for i, (user_id, data) in enumerate(top5, start=1):
            medal = medals[i-1] if i <= 3 else f"{i}."
            description += f"{medal} {data['pseudo']} ({data['score']} pts)\n"

        embed.description = description
        await interaction.response.send_message(embed=embed)

# Async setup pour slash commands
async def setup(bot):
    await bot.add_cog(Enigmes(bot))
