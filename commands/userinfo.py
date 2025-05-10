import discord
from discord.ext import commands
from discord import app_commands


class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="userinfo", description="Affiche les infos d'un utilisateur")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member):
        embed = discord.Embed(title=f"Infos de {member}", color=discord.Color.blue())
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Rejoint le", value=member.joined_at.strftime("%d/%m/%Y"))
        embed.add_field(name="Compte créé le", value=member.created_at.strftime("%d/%m/%Y"))
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(UserInfo(bot))
