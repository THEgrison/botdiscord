from discord.ext import commands
from discord import app_commands, Interaction, Embed, Color


class ParleCog(commands.Cog):
    """Cog permettant au bot de répéter les messages d'un administrateur"""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="parle",
        description=
        "Fait parler le bot en répétant le message d'un administrateur")
    async def parle(self, interaction: Interaction, message: str = None):
        """Fait parler le bot et supprime le message de commande de l'utilisateur. Si aucun message n'est fourni, affiche l'aide."""

        # Si aucun message n'est donné, affiche l'embed d'aide
        if message is None:
            embed = Embed(
                title="🔊 Commande 'Parle' - Aide",
                description=
                "Cette commande permet aux administrateurs de faire parler le bot et de supprimer leur message de commande.",
                color=Color.green())

            embed.add_field(
                name="📝 Utilisation :",
                value="`/parle <message>` → Le bot répétera ce message.",
                inline=False)

            embed.add_field(
                name="⚠️ Restrictions :",
                value=
                "Cette commande est uniquement disponible pour les **administrateurs**.",
                inline=False)

            embed.add_field(
                name="🧑‍💻 Exemple :",
                value=
                "`/parle Bonjour à tous !` → Le bot répondra par 'Bonjour à tous !'.",
                inline=False)

            embed.set_footer(
                text="📌 Utilise /help pour voir toutes les commandes du bot.")

            await interaction.response.send_message(embed=embed)

        # Si un message est donné, fait parler le bot et supprime le message
        else:
            # Vérifie si l'utilisateur a les permissions nécessaires
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message(
                    "❌ Vous devez être administrateur pour utiliser cette commande."
                )
                return

            # Le bot répond avec le message de l'utilisateur
            await interaction.response.send_message(message)


async def setup(bot):
    """Charge le cog ParleCog dans le bot."""
    await bot.add_cog(ParleCog(bot))
