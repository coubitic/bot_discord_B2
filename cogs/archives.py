import discord
from discord.ext import commands
from discord import app_commands
import json
import os

USERS_FILE = "data/users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

class Archives(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="profil",
        description="Consulte votre profil archéologique personnel"
    )
    async def profile(self, interaction: discord.Interaction):
        users = load_users()
        user_id = str(interaction.user.id)

        # Initialisation minimale si l'utilisateur n'existe pas
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
        guilds = len(user.get("guilds", []))

        # Détermination du titre selon le score
        if score >= 20:
            titre = "🏛️ Conservateur des mythes"
        elif score >= 10:
            titre = "🗿 Archéologue"
        elif score >= 5:
            titre = "🧭 Explorateur"
        else:
            titre = "📖 Novice"

        embed = discord.Embed(
            title=f"📜 Profil de {interaction.user.name}",
            color=discord.Color.dark_gold()
        )

        embed.add_field(
            name="🧩 Énigmes découvertes :",
            value=str(enigmes_resolues),
            inline=True
        )
        embed.add_field(
            name="⭐ Score total :",
            value=str(score),
            inline=True
        )
        embed.add_field(
            name="🏷️ Statut archéologique :",
            value=titre,
            inline=False
        )

        embed.set_footer(text="Votre profil conserve la mémoire de vos découvertes.")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Archives(bot))
