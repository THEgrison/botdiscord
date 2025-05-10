import discord
from discord.ext import commands
from discord import app_commands


class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="serverinfo", description="Affiche les infos du serveur")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(title=f"Infos du serveur : {guild.name}", color=discord.Color.green())
        embed.add_field(name="📅 Créé le", value=guild.created_at.strftime("%d/%m/%Y"), inline=False)
        embed.add_field(name="👥 Membres", value=guild.member_count, inline=True)
        embed.add_field(name="🔧 Rôles", value=len(guild.roles), inline=True)
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(ServerInfo(bot))
