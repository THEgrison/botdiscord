import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import random
import html

class QuizAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="quiz", description="Pose une question aléatoire depuis une API.")
    async def quiz(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://opentdb.com/api.php?amount=1&type=multiple") as response:
                data = await response.json()

        question_data = data['results'][0]
        question = html.unescape(question_data["question"])
        correct_answer = html.unescape(question_data["correct_answer"])
        options = [html.unescape(ans) for ans in question_data["incorrect_answers"]]
        options.append(correct_answer)
        random.shuffle(options)

        view = discord.ui.View(timeout=15)

        for option in options:
            button = discord.ui.Button(label=option)

            async def callback(interact: discord.Interaction, selected=option):
                if selected == correct_answer:
                    await interact.response.send_message("Bonne réponse ! 🎉", ephemeral=True)
                else:
                    await interact.response.send_message(f"Faux 😢 La bonne réponse était : {correct_answer}", ephemeral=True)
                view.stop()

            button.callback = callback
            view.add_item(button)

        await interaction.response.send_message(f"🧠 **{question}**", view=view)

async def setup(bot):
    await bot.add_cog(QuizAPI(bot))
