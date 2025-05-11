import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime


class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="serverinfo", description="Affiche des informations détaillées sur le serveur")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild

        try:
            embed = discord.Embed(
                title=f"📊 Informations sur le serveur : {guild.name}",
                color=discord.Color.blurple(),
                timestamp=datetime.utcnow()
            )

            # Informations générales
            embed.add_field(name="📅 Création du serveur", value=guild.created_at.strftime("%d %B %Y à %H:%M:%S"), inline=False)
            embed.add_field(name="👑 Propriétaire", value=guild.owner.mention, inline=True)
            embed.add_field(name="🆔 ID du serveur", value=guild.id, inline=True)

            # Statistiques membres
            total_members = guild.member_count
            humans = len([m for m in guild.members if not m.bot])
            bots = total_members - humans
            embed.add_field(name="👥 Membres", value=f"Total : {total_members}\n👤 Humains : {humans}\n🤖 Bots : {bots}", inline=False)

            # Statistiques de salons
            text_channels = len(guild.text_channels)
            voice_channels = len(guild.voice_channels)
            categories = len(guild.categories)
            embed.add_field(name="💬 Salons", value=f"📝 Textes : {text_channels}\n🔊 Vocaux : {voice_channels}\n📁 Catégories : {categories}", inline=False)

            # Rôles
            roles = len(guild.roles)
            embed.add_field(name=f"🏷️ Nombre de rôles", value=str(roles), inline=True)

            # Emojis
            emojis = len(guild.emojis)
            stickers = len(guild.stickers)
            embed.add_field(name="😄 Emojis & Stickers", value=f"{emojis} emojis, {stickers} stickers", inline=True)

            # Boost
            boost_level = guild.premium_tier
            boosters = guild.premium_subscription_count
            embed.add_field(name="🚀 Boost", value=f"Niveau {boost_level} ({boosters} boosts)", inline=False)

            # Icône
            if guild.icon:
                embed.set_thumbnail(url=guild.icon.url)

            # Pied de page
            embed.set_footer(text=f"Demandé par {interaction.user}", icon_url=interaction.user.display_avatar.url)

            await interaction.response.send_message(embed=embed)

        except discord.DiscordException as e:
            await interaction.response.send_message(f"❌ Une erreur s'est produite lors de la récupération des informations du serveur : {e}")

async def setup(bot):
    await bot.add_cog(ServerInfo(bot))
