import discord
from discord import app_commands
from discord.ext import commands

class Unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="unban", description="Débannit un utilisateur par ID.")
    @app_commands.describe(user_id="L'ID de l'utilisateur à débannir.")
    async def unban(self, interaction: discord.Interaction, user_id: str):
        try:
            user = await self.bot.fetch_user(int(user_id))
            await interaction.guild.unban(user)
            await interaction.response.send_message(f"{user} a été débanni.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Erreur : {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Unban(bot))
