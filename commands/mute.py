import discord
from discord.ext import commands
from discord import app_commands
import datetime

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mute", description="Rend muet un utilisateur pendant une durée donnée.")
    @app_commands.describe(user="Utilisateur à rendre muet", duration="Durée (en secondes)")
    async def mute(self, interaction: discord.Interaction, user: discord.Member, duration: int):
        try:
            await user.timeout(datetime.timedelta(seconds=duration))
            await interaction.response.send_message(f"{user.mention} a été mute pour {duration} secondes.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Erreur : {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Mute(bot))
