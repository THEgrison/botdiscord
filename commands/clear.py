import discord
from discord.ext import commands
from discord import app_commands


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="Supprime un nombre de messages dans le salon")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, nombre: int):
        if nombre <= 0:
            await interaction.response.send_message("❌ Le nombre de messages doit être supérieur à 0.", ephemeral=True)
            return

        await interaction.channel.purge(limit=nombre)
        await interaction.response.send_message(f"🧹 {nombre} message(s) supprimé(s).", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Clear(bot))
