import discord
from discord.ext import commands
from discord import app_commands
import random

class Guess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="guess", description="Devine un nombre entre 1 et 10.")
    @app_commands.describe(number="Le nombre que tu veux deviner (entre 1 et 10).")
    async def guess(self, interaction: discord.Interaction, number: int):
        if number < 1 or number > 10:
            await interaction.response.send_message("Choisis un nombre entre 1 et 10 !", ephemeral=True)
            return

        secret = random.randint(1, 10)
        if number == secret:
            await interaction.response.send_message(f"Bravo ! Tu as trouvé 🎉 (c'était bien {secret})")
        else:
            await interaction.response.send_message(f"Raté 😢 Le bon nombre était {secret}.")

async def setup(bot):
    await bot.add_cog(Guess(bot))
