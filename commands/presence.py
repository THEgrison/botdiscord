import discord
from discord.ext import commands
from discord import app_commands, ActivityType, Embed, Color, Status, Streaming, Activity


class Presence(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Définit un statut par défaut au démarrage"""
        await self.bot.change_presence(
            activity=discord.Game(name="/help | Regarde Black Bear TV"),
            status=discord.Status.online)

    @app_commands.command(name="setpresence",
                          description="Change la présence du bot.")
    async def setpresence(self,
                          interaction: discord.Interaction,
                          ptype: str = None,
                          *,
                          text: str = None):
        """
        Change la présence du bot via slash command.
        Utilisation : /setpresence [game|stream|listen|watch] [texte]
        """
        if not ptype or not text:
            embed = Embed(title="🛠️ Commande SetPresence",
                          description="Permet de modifier la présence du bot.",
                          color=Color.blue())
            embed.add_field(
                name="📌 Utilisation :",
                value="/setpresence [game|stream|listen|watch] [texte]",
                inline=False)
            embed.add_field(name="📖 Exemple :",
                            value="/setpresence game Je joue à Minecraft",
                            inline=False)
            embed.set_footer(text="Black Bear Bot - Présence personnalisée")
            await interaction.response.send_message(embed=embed)
            return

        status_type = {
            "game":
            discord.Game(name=text),  # Joue à
            "stream":
            discord.Streaming(
                name=text,
                url="https://www.twitch.tv/nom_du_stream"),  # Stream
            "listen":
            discord.Activity(type=discord.ActivityType.listening,
                             name=text),  # Écoute
            "watch":
            discord.Activity(type=discord.ActivityType.watching,
                             name=text)  # Regarde
        }

        if ptype.lower() not in status_type:
            await interaction.response.send_message(
                "⚠️ Type invalide ! Utilise : game, stream, listen, watch.")
            return

        await self.bot.change_presence(activity=status_type[ptype.lower()],
                                       status=discord.Status.online)
        await interaction.response.send_message(
            f"✅ Présence mise à jour : **{ptype.capitalize()} {text}**")

    @app_commands.command(
        name="custompresence",
        description="Met à jour la présence avec des détails personnalisés.")
    async def custompresence(self,
                             interaction: discord.Interaction,
                             details: str = None,
                             state: str = None,
                             large_image: str = None,
                             small_image: str = None,
                             party_size: int = None,
                             party_max: int = None,
                             join_secret: str = None):
        """
        Met à jour la présence avec des détails personnalisés via slash command.
        Utilisation : /custompresence [details] [state] [large_image] [small_image] [party_size] [party_max] [join_secret]
        """
        if not all([
                details, state, large_image, small_image, party_size,
                party_max, join_secret
        ]):
            embed = Embed(
                title="🎨 Commande CustomPresence",
                description=
                "Personnalise la présence du bot avec des détails avancés.",
                color=Color.blue())
            embed.add_field(
                name="📌 Utilisation :",
                value=
                "/custompresence [details] [state] [large_image] [small_image] [party_size] [party_max] [join_secret]",
                inline=False)
            embed.add_field(
                name="📖 Exemple :",
                value=
                "/custompresence Jouer En ligne image_grande image_petite 3 10 secret_code",
                inline=False)
            embed.set_footer(text="Black Bear Bot - Présence avancée")
            await interaction.response.send_message(embed=embed)
            return

        discordPresence = discord.Activity(
            type=discord.ActivityType.
            playing,  # Peut être changé en stream, listen, watch
            name=details)

        discordPresence.start = 1507665886  # Exemple de timestamp de début
        discordPresence.end = 1507665886  # Exemple de timestamp de fin

        discordPresence.large_image = large_image
        discordPresence.small_image = small_image
        discordPresence.large_text = "Numbani"  # Exemple
        discordPresence.small_text = f"Rogue - Level {party_size}"  # Exemple basé sur la taille du groupe
        discordPresence.party_size = party_size
        discordPresence.party_max = party_max
        discordPresence.join_secret = join_secret

        await self.bot.change_presence(activity=discordPresence,
                                       status=discord.Status.online)
        await interaction.response.send_message(
            f"✅ Présence personnalisée mise à jour avec {details}, état: {state}."
        )


async def setup(bot):
    await bot.add_cog(Presence(bot))
