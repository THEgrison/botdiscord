import discord
from discord.ext import commands
from discord import app_commands
import random

class RPS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="rps", description="Pierre, feuille, ciseaux contre le bot.")
    @app_commands.choices(choice=[
        app_commands.Choice(name="Pierre", value="pierre"),
        app_commands.Choice(name="Feuille", value="feuille"),
        app_commands.Choice(name="Ciseaux", value="ciseaux")
    ])
    async def rps(self, interaction: discord.Interaction, choice: app_commands.Choice[str]):
        bot_choice = random.choice(["pierre", "feuille", "ciseaux"])
        user = choice.value

        if user == bot_choice:
            result = "Égalité !"
        elif (user == "pierre" and bot_choice == "ciseaux") or \
             (user == "feuille" and bot_choice == "pierre") or \
             (user == "ciseaux" and bot_choice == "feuille"):
            result = "Tu gagnes ! 🎉"
        else:
            result = "Tu perds ! 😢"

        await interaction.response.send_message(f"Tu as choisi **{user}**, le bot a choisi **{bot_choice}**. {result}")

async def setup(bot):
    await bot.add_cog(RPS(bot))
