import discord
from discord.ext import commands
from discord import app_commands


class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Expulse un membre du serveur")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Aucune raison spécifiée"):
        # Vérifie si le bot peut expulser le membre
        if not interaction.guild.me.guild_permissions.kick_members:
            await interaction.response.send_message("❌ Je n'ai pas la permission d'expulser des membres.", ephemeral=True)
            return

        # Empêche certaines expulsions
        if member.id == interaction.user.id:
            await interaction.response.send_message("❌ Tu ne peux pas t'expulser toi-même.", ephemeral=True)
            return
        if member.id == self.bot.user.id:
            await interaction.response.send_message("❌ Tu ne peux pas expulser le bot.", ephemeral=True)
            return

        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="👢 Membre expulsé",
                description=f"{member.mention} a été expulsé du serveur.",
                color=discord.Color.orange()
            )
            embed.add_field(name="Raison", value=reason, inline=False)
            await interaction.response.send_message(embed=embed)

        except discord.Forbidden:
            await interaction.response.send_message("❌ Je ne peux pas expulser ce membre (rôle trop haut ?)", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"⚠️ Une erreur est survenue : `{e}`", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Kick(bot))
