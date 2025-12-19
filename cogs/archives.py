import discord
from discord.ext import commands
from discord import app_commands

class Archives(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping_archives", description="Teste le cog Archives")
    async def ping_archives(self, interaction: discord.Interaction):
        await interaction.response.send_message("Cog archives actif ✅")

async def setup(bot):
    await bot.add_cog(Archives(bot))
