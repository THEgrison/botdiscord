import discord
from discord.ext import commands
from discord import app_commands


class TodoList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.todo_lists = {}

    @app_commands.command(name="todolist", description="Affiche la liste de tes tâches")
    async def todolist(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        tasks = self.todo_lists.get(user_id, [])

        if not tasks:
            await interaction.response.send_message("📭 Ta liste de tâches est vide.", ephemeral=True)
        else:
            embed = discord.Embed(title="📝 Ta liste de tâches", color=discord.Color.teal())
            for i, task in enumerate(tasks, 1):
                embed.add_field(name=f"Tâche {i}", value=task, inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    # Permet de synchroniser les listes entre le /todo et le /todolist
    @commands.Cog.listener()
    async def on_cog_add(self, cog):
        if cog.__class__.__name__ == "Todo":
            self.todo_lists = cog.todo_lists


async def setup(bot):
    await bot.add_cog(TodoList(bot))
