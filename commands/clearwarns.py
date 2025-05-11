import discord
from discord.ext import commands
from discord import app_commands


class ClearWarns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warns = bot.get_cog("Warn").warnings  # Récupère les avertissements du cog Warn

    @app_commands.command(name="clearwarns", description="Supprime tous les avertissements d’un membre")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clearwarns(self, interaction: discord.Interaction, member: discord.Member):
        if member.id not in self.warns or len(self.warns[member.id]) == 0:
            await interaction.response.send_message(f"{member.mention} n’a aucun avertissement à supprimer.", ephemeral=True)
            return

        del self.warns[member.id]

        await interaction.response.send_message(f"✅ Tous les avertissements de {member.mention} ont été supprimés.")


async def setup(bot):
    await bot.add_cog(ClearWarns(bot))
