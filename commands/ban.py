import discord
from discord.ext import commands
from discord import app_commands


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ban", description="Bannit un membre du serveur")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Aucune raison spécifiée"):
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="🔨 Membre banni",
                description=f"{member.mention} a été banni.",
                color=discord.Color.red()
            )
            embed.add_field(name="Raison", value=reason, inline=False)
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message("❌ Je n'ai pas la permission de bannir ce membre.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"⚠️ Une erreur est survenue : {e}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Ban(bot))
