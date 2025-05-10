import discord
import json
from discord.ext import commands
from discord import app_commands


class AltDetector(commands.Cog):
    """Détecte les comptes secondaires (alts) sur le serveur"""

    def __init__(self, bot):
        self.bot = bot
        self.data_file = "alt_data.json"
        self.users = self.load_data()

    def load_data(self):
        """Charge les données enregistrées"""
        try:
            with open(self.data_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_data(self):
        """Sauvegarde les données dans un fichier"""
        with open(self.data_file, "w") as f:
            json.dump(self.users, f, indent=4)

    async def track_user(self, member: discord.Member):
        """Ajoute un utilisateur à la base de données pour le suivi"""
        guild_id = str(member.guild.id)
        user_id = str(member.id)

        if guild_id not in self.users:
            self.users[guild_id] = {}

        if user_id not in self.users[guild_id]:
            self.users[guild_id][user_id] = {
                "name": member.name,
                "discriminator": member.discriminator,
                "avatar": str(member.avatar),
                "joined_at": str(member.joined_at),
                "created_at": str(member.created_at),
            }
            self.save_data()

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Détecte si un compte similaire a déjà rejoint le serveur"""
        await self.track_user(member)

        guild_id = str(member.guild.id)
        user_id = str(member.id)
        possible_alts = []

        for existing_id, data in self.users.get(guild_id, {}).items():
            if existing_id != user_id:
                if (data["name"] == member.name and data["discriminator"]
                        == member.discriminator) or (data["avatar"] == str(
                            member.avatar)):
                    possible_alts.append(f"<@{existing_id}>")

        if possible_alts:
            alert_message = (
                f"⚠️ **Alt détecté !** {member.mention} semble être un alt de :\n"
                + ", ".join(possible_alts))
            mod_channel = discord.utils.get(
                member.guild.text_channels,
                name="│👥・logs-membres")  # Modifier selon besoin
            if mod_channel:
                await mod_channel.send(alert_message)

    @app_commands.command(
        name="checkalt",
        description="Vérifie si un utilisateur a des comptes secondaires connus"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def checkalt(self, interaction: discord.Interaction,
                       user: discord.Member):
        """Vérifie si un utilisateur a des comptes secondaires connus via slash command"""
        guild_id = str(interaction.guild.id)
        user_id = str(user.id)
        alts = []

        for existing_id, data in self.users.get(guild_id, {}).items():
            if existing_id != user_id:
                if (data["name"] == user.name and data["discriminator"]
                        == user.discriminator) or (data["avatar"] == str(
                            user.avatar)):
                    alts.append(f"<@{existing_id}>")

        if alts:
            await interaction.response.send_message(
                f"🔍 **Alt trouvés pour {user.mention}** : " + ", ".join(alts))
        else:
            await interaction.response.send_message(
                f"✅ {user.mention} ne semble pas avoir d'alt détecté.")


async def setup(bot):
    """Charge le cog AltDetector dans le bot."""
    await bot.add_cog(AltDetector(bot))
