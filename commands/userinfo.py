import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime


class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="userinfo", description="Affiche des informations détaillées sur un membre")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user

        embed = discord.Embed(
            title=f"ℹ️ Informations sur {member.name}",
            color=member.color,
            timestamp=datetime.utcnow()
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        # ID, pseudo, et tag
        embed.add_field(name="🆔 ID", value=member.id, inline=True)
        embed.add_field(name="📛 Nom d'utilisateur", value=f"{member}", inline=True)
        embed.add_field(name="🖼️ Avatar", value=f"[Lien direct]({member.display_avatar.url})", inline=False)

        # Statuts
        embed.add_field(name="📱 Statut", value=str(member.status).capitalize(), inline=True)
        embed.add_field(name="🖥️ Activité", value=member.activity.name if member.activity else "Aucune", inline=True)

        # Rôles
        roles = [role.mention for role in member.roles if role != interaction.guild.default_role]
        embed.add_field(name=f"🏷️ Rôles ({len(roles)})", value=", ".join(roles) if roles else "Aucun", inline=False)

        # Dates
        embed.add_field(name="📆 Créé le", value=member.created_at.strftime("%d %B %Y à %H:%M"), inline=True)
        embed.add_field(name="🔔 Rejoint le", value=member.joined_at.strftime("%d %B %Y à %H:%M") if member.joined_at else "Inconnu", inline=True)

        # Boost
        if member.premium_since:
            embed.add_field(name="🚀 Boost le serveur depuis", value=member.premium_since.strftime("%d %B %Y"), inline=False)

        # Bot ?
        embed.set_footer(text="🤖 C'est un bot" if member.bot else "👤 C'est un utilisateur humain")

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(UserInfo(bot))
