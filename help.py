import discord
from discord.ext import commands
from discord import app_commands, Embed, Color, Interaction


class HelpCog(commands.Cog):
    """Cog pour une commande d'aide personnalisée"""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="help",
        description="Affiche une aide personnalisée sous forme d'embed")
    async def help_command(self, interaction: Interaction):
        """Affiche une aide personnalisée sous forme d'embed"""

        embed = Embed(
            title="📜 Liste des Commandes",
            description="Voici les commandes disponibles :",
            color=Color(0xFFFFFF)  # Blanc en hexadécimal
        )

        # Lister les commandes slash enregistrées
        for command in self.bot.tree.walk_commands():
            embed.add_field(name=f"❓ {command.name}",
                            value=command.description or "Pas de description",
                            inline=False)

        embed.set_footer(text="")

        await interaction.response.send_message(embed=embed)


# Fonction pour charger le cog
async def setup(bot):
    await bot.add_cog(HelpCog(bot))
