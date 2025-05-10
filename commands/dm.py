import discord
from discord.ext import commands
from discord import app_commands


class DmCog(commands.Cog):
    """Cog permettant d'envoyer un message privé à un utilisateur et de recevoir une réponse"""

    def __init__(self, bot):
        self.bot = bot
        self.pending_dms = {
        }  # Dictionnaire pour stocker qui a envoyé le message initial

    @app_commands.command(
        name="dm", description="Envoie un message privé à un utilisateur")
    @app_commands.checks.has_permissions(administrator=True)
    async def dm(self, interaction: discord.Interaction,
                 member: discord.Member, message: str):
        """Envoie un message privé à un utilisateur et affiche l'aide si aucun argument n'est fourni"""

        try:
            # Envoie du message privé
            dm_embed = discord.Embed(
                title="📩 Nouveau message d'un administrateur",
                description=f"**Message :**\n{message}",
                color=discord.Color.blue())

            await member.send(embed=dm_embed)

            # Stocke l'auteur du message initial pour suivre les réponses
            self.pending_dms[member.id] = interaction.user.id

            # Confirmation à l'admin
            confirmation_embed = discord.Embed(
                title="📩 Message envoyé",
                description=f"Le message a bien été envoyé à {member.mention}.",
                color=discord.Color.green())
            confirmation_embed.add_field(name="📝 Message :",
                                         value=message,
                                         inline=False)
            confirmation_embed.set_footer(
                text="Commande réservée aux administrateurs.")

            await interaction.response.send_message(embed=confirmation_embed)

        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Impossible d'envoyer un message privé à cet utilisateur (DM fermés)."
            )
        except Exception as e:
            await interaction.response.send_message(f"⚠️ Erreur : {e}")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Gère les réponses aux messages privés du bot"""

        # Vérifie si c'est un DM et que ce n'est pas le bot lui-même
        if message.guild is None and not message.author.bot:
            if message.author.id in self.pending_dms:
                admin_id = self.pending_dms[message.author.id]
                admin = self.bot.get_user(admin_id)

                if admin:
                    response_embed = discord.Embed(
                        title="📩 Réponse reçue",
                        description=
                        f"**De {message.author.mention} :**\n{message.content}",
                        color=discord.Color.orange())
                    response_embed.set_footer(
                        text="Réponse automatique du bot")

                    await admin.send(embed=response_embed)


async def setup(bot):
    """Charge le cog DmCog dans le bot."""
    await bot.add_cog(DmCog(bot))
