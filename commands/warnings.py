import discord
from discord.ext import commands
from discord import app_commands

class Warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="warnings", description="Affiche les avertissements d’un membre")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warnings(self, interaction: discord.Interaction, member: discord.Member):
        warn_cog = self.bot.get_cog("Warn")
        if warn_cog is None:
            await interaction.response.send_message("❌ Le système d'avertissements (Warn) n'est pas chargé.", ephemeral=True)
            return

        warns = warn_cog.warnings
        user_warns = warns.get(str(member.id))

        if not user_warns:
            await interaction.response.send_message(f"✅ {member.mention} n'a aucun avertissement.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"📋 Avertissements de {member}",
            color=discord.Color.orange()
        )

        for i, warn in enumerate(user_warns, start=1):
            embed.add_field(
                name=f"⚠️ Avertissement {i}",
                value=f"**Modérateur :** {warn['mod']}\n**Raison :** {warn['reason']}",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Warnings(bot))
