import discord
from discord.ext import commands
from discord import app_commands
import random

class Fact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    facts = [
        "Les chats dorment en moyenne 16 heures par jour.",
        "L'espace est complètement silencieux.",
        "Le cœur d’une crevette est situé dans sa tête.",
        "Un éclair est cinq fois plus chaud que le soleil.",
        "Le miel ne périme jamais."
    ]

    @app_commands.command(name="fact", description="Envoie un fait intéressant aléatoire.")
    async def fact(self, interaction: discord.Interaction):
        await interaction.response.send_message(random.choice(self.facts))

async def setup(bot):
    await bot.add_cog(Fact(bot))
