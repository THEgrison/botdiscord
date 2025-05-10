import discord
from discord.ext import commands
from discord import app_commands
import time


class PingCog(commands.Cog):
    """Cog pour la commande Ping qui renvoie Pong et mesure le temps de latence"""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ping", description="Renvoie Pong et mesure le temps de latence")
    async def ping(self, interaction: discord.Interaction):
        """Mesure le temps de latence du bot"""

        # Enregistrer le temps avant l'envoi de la réponse
        start_time = time.time()

        # Envoie une réponse et mesure le temps de latence
        await interaction.response.send_message("Pong!")

        # Calcul du temps de latence (temps entre l'envoi du message et la réponse)
        latency = (time.time() -
                   start_time) * 1000  # Convertir en millisecondes

        # Mettre à jour le message avec le temps de latence
        await interaction.edit_original_response(
            content=f"Pong! Latence : {latency:.2f}ms")


# Fonction pour charger le cog
async def setup(bot):
    """Charge le cog PingCog dans le bot."""
    await bot.add_cog(PingCog(bot))
