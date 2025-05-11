import discord
from discord.ext import commands
from discord import app_commands

class ClearWarns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clearwarns", description="Supprime tous les avertissements d’un membre")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clearwarns(self, interaction: discord.Interaction, member: discord.Member):
        warn_cog = self.bot.get_cog("Warn")

        if warn_cog is None:
            await interaction.response.send_message("❌ Le système d'avertissements (Warn) n'est pas chargé.", ephemeral=True)
            return

        warns = warn_cog.warnings
        save = warn_cog.save_warnings

        if str(member.id) not in warns or len(warns[str(member.id)]) == 0:
            await interaction.response.send_message(f"{member.mention} n’a aucun avertissement à supprimer.", ephemeral=True)
            return

        del warns[str(member.id)]
        save()

        await interaction.response.send_message(f"✅ Tous les avertissements de {member.mention} ont été supprimés.")

async def setup(bot):
    await bot.add_cog(ClearWarns(bot))
