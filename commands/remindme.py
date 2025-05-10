import discord
from discord.ext import commands
from discord import app_commands
import asyncio


class RemindMe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="remindme", description="Crée un rappel privé dans quelques minutes")
    async def remindme(self, interaction: discord.Interaction, texte: str, minutes: int):
        await interaction.response.send_message(
            f"⏰ Rappel programmé dans {minutes} minute(s) : **{texte}**", ephemeral=True
        )

        await asyncio.sleep(minutes * 60)

        try:
            await interaction.user.send(f"🔔 Rappel : {texte}")
        except discord.Forbidden:
            await interaction.followup.send("❌ Impossible d'envoyer un rappel en message privé.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(RemindMe(bot))
