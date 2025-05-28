import discord
from discord.ext import commands
from discord import app_commands

class Whois(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="whois", description="Affiche les informations d'un utilisateur.")
    @app_commands.describe(user="Le membre à inspecter")
    async def whois(self, interaction: discord.Interaction, user: discord.User):
        member = interaction.guild.get_member(user.id)

        embed = discord.Embed(title=f"Informations sur {user.name}", color=discord.Color.blue())
        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
        embed.add_field(name="Tag", value=f"`{user}`", inline=True)
        embed.add_field(name="ID", value=f"`{user.id}`", inline=True)
        embed.add_field(
            name="Compte créé le",
            value=discord.utils.format_dt(user.created_at, style="F"),
            inline=False
        )

        if member:
            embed.add_field(
                name="Rejoint le serveur",
                value=discord.utils.format_dt(member.joined_at, style="F"),
                inline=False
            )
            roles = [role.mention for role in member.roles[1:]]  # ignore @everyone
            embed.add_field(
                name=f"Rôles ({len(roles)})",
                value=", ".join(roles) if roles else "Aucun",
                inline=False
            )
        else:
            embed.add_field(name="Statut", value="L'utilisateur n'est pas sur ce serveur.", inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Whois(bot))
