import discord
from discord.ext import commands
from discord import app_commands
import random

class RPS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    rps_choices = [
        app_commands.Choice(name="Pierre", value="pierre"),
        app_commands.Choice(name="Feuille", value="feuille"),
        app_commands.Choice(name="Ciseaux", value="ciseaux")
    ]

    @app_commands.command(name="rps", description="Pierre, feuille, ciseaux contre le bot.")
    @app_commands.describe(choice="Ton choix : pierre, feuille ou ciseaux")
    async def rps(self, interaction: discord.Interaction, choice: str):
        if choice not in ["pierre", "feuille", "ciseaux"]:
            await interaction.response.send_message("❌ Choix invalide. Utilise : pierre, feuille ou ciseaux.", ephemeral=True)
            return

        bot_choice = random.choice(["pierre", "feuille", "ciseaux"])

        if choice == bot_choice:
            result = "Égalité !"
        elif (choice == "pierre" and bot_choice == "ciseaux") or \
             (choice == "feuille" and bot_choice == "pierre") or \
             (choice == "ciseaux" and bot_choice == "feuille"):
            result = "Tu gagnes ! 🎉"
        else:
            result = "Tu perds ! 😢"

        await interaction.response.send_message(
            f"Tu as choisi **{choice}**, le bot a choisi **{bot_choice}**. {result}"
        )

    async def cog_load(self):
        self.rps.autocomplete("choice")(self.autocomplete_choice)

    async def autocomplete_choice(self, interaction: discord.Interaction, current: str):
        choices = ["pierre", "feuille", "ciseaux"]
        return [
            app_commands.Choice(name=word.title(), value=word)
            for word in choices if current.lower() in word
        ]

async def setup(bot):
    await bot.add_cog(RPS(bot))
