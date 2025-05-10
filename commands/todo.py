import discord
from discord.ext import commands
from discord import app_commands


class Todo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.todo_lists = {}

    @app_commands.command(name="todo", description="Ajoute une tâche à faire")
    async def todo(self, interaction: discord.Interaction, tache: str):
        user_id = interaction.user.id
        if user_id not in self.todo_lists:
            self.todo_lists[user_id] = []

        self.todo_lists[user_id].append(tache)
        await interaction.response.send_message(
            f"📝 Tâche ajoutée à ta liste : **{tache}**", ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Todo(bot))
