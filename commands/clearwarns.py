import discord
from discord.ext import commands
from discord import app_commands

class ClearWarns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warns = bot.get_cog("Warn").warnings  # Accéder aux avertissements chargés depuis le cog Warn
        self.save = bot.get_cog("Warn").save_warnings  # Sauvegarder les avertissements après suppression

    @app_commands.command(name="clearwarns", description="Supprime tous les avertissements d’un membre")
    @app_commands.checks.has_permissions(manage_messages=True)  # Vérifie que l'utilisateur a les permissions nécessaires
    async def clearwarns(self, interaction: discord.Interaction, member: discord.Member):
        # Vérifier si le membre a des avertissements
        if str(member.id) not in self.warns or len(self.warns[str(member.id)]) == 0:
            await interaction.response.send_message(
                f"{member.mention} n’a aucun avertissement à supprimer.", ephemeral=True
            )
            return

        # Supprimer tous les avertissements du membre
        del self.warns[str(member.id)]  # Supprimer les avertissements du membre
        self.save()  # Sauvegarder les modifications

        await interaction.response.send_message(
            f"✅ Tous les avertissements de {member.mention} ont été supprimés."
        )

async def setup(bot):
    await bot.add_cog(ClearWarns(bot))
