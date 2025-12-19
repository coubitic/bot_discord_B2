import discord
from discord.ext import commands
from discord import app_commands
import random
import json

class Enigmes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.enigmes_en_cours = {}
        with open("data/enigmes.json", "r", encoding="utf-8") as f:
            self.enigmes = json.load(f)

    @app_commands.command(name="enigme", description="Pose une énigme mythologique")
    async def enigme(self, interaction: discord.Interaction):
        enigme = random.choice(self.enigmes)
        self.enigmes_en_cours[interaction.user.id] = enigme
        await interaction.response.send_message(f"🧩 **Énigme** : {enigme['question']}")

    @app_commands.command(name="reponse", description="Répond à l'énigme en cours")
    async def reponse(self, interaction: discord.Interaction, reponse: str):
        user_id = interaction.user.id
        if user_id not in self.enigmes_en_cours:
            await interaction.response.send_message("❌ Vous n'avez pas d'énigme en cours.")
            return

        enigme = self.enigmes_en_cours[user_id]
        if reponse.lower() == enigme["reponse"].lower():
            await interaction.response.send_message("✅ Bonne réponse !")
            del self.enigmes_en_cours[user_id]
        else:
            await interaction.response.send_message(f"❌ Mauvaise réponse. Indice : {enigme['indice']}")

# Async setup pour slash commands
async def setup(bot):
    await bot.add_cog(Enigmes(bot))
