import discord
from discord.ext import commands
from discord import app_commands
import random


class CoinFlip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="coinflip", description="Lance une pièce : pile ou face")
    async def coinflip(self, interaction: discord.Interaction):
        result = random.choice(["🪙 Pile", "🪙 Face"])
        await interaction.response.send_message(f"Résultat : **{result}**")


async def setup(bot):
    await bot.add_cog(CoinFlip(bot))
