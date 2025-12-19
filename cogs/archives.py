import discord
from discord.ext import commands
from discord import app_commands

class Archives(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Async setup pour slash commands
async def setup(bot):
    await bot.add_cog(Archives(bot))
