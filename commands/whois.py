import discord
from discord.ext import commands
from discord import app_commands

class Whois(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="whois", description="Affiche les informations d'un membre.")
    @app_commands.describe(user="Le membre à inspecter")
    async def whois(self, interaction: discord.Interaction, user: discord.Member):
        embed = discord.Embed(
            title=f"Informations sur {user}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="Tag", value=f"`{user}`", inline=True)
        embed.add_field(name="ID", value=f"`{user.id}`", inline=True)
        embed.add_field(
            name="Compte créé le",
            value=discord.utils.format_dt(user.created_at, style="F"),
            inline=False
        )
        embed.add_field(
            name="Rejoint le serveur",
            value=discord.utils.format_dt(user.joined_at, style="F") if user.joined_at else "Inconnu",
            inline=False
        )

        roles = [role.mention for role in user.roles[1:]]  # Ignore @everyone
        embed.add_field(
            name=f"Rôles ({len(roles)})",
            value=", ".join(roles) if roles else "Aucun",
            inline=False
        )

        await interaction.response.send_message(embed=embed)

    async def cog_load(self):
        self.bot.tree.add_command(self.whois)


async def setup(bot):
    await bot.add_cog(Whois(bot))
