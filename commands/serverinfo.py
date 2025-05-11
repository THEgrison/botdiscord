import discord
from discord.ext import commands
from discord import app_commands

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="serverinfo", description="Affiche des informations sur le serveur.")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild  # Récupère le serveur (guild)
        
        # Préparer les informations à afficher
        embed = discord.Embed(title=f"Informations sur {guild.name}", color=discord.Color.blue())
        embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)  # Icône du serveur
        embed.add_field(name="Nom du serveur", value=guild.name, inline=False)
        embed.add_field(name="ID du serveur", value=guild.id, inline=False)
        embed.add_field(name="Propriétaire", value=f"{guild.owner}", inline=False)
        embed.add_field(name="Région", value=guild.region, inline=False)
        embed.add_field(name="Nombre de membres", value=len(guild.members), inline=False)
        embed.add_field(name="Nombre de salons", value=len(guild.channels), inline=False)
        embed.add_field(name="Nombre de rôles", value=len(guild.roles), inline=False)
        embed.add_field(name="Date de création", value=guild.created_at.strftime("%d %b %Y"), inline=False)
        
        # Envoi du message
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerInfo(bot))
