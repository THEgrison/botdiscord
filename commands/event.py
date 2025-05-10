import discord
from discord.ext import commands
from discord import app_commands


class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="event", description="Crée un événement avec une date et une description")
    async def event(self, interaction: discord.Interaction, date: str, description: str):
        embed = discord.Embed(
            title="📅 Nouvel événement",
            description=description,
            color=discord.Color.gold()
        )
        embed.add_field(name="📆 Date", value=date, inline=False)
        embed.set_footer(text=f"Créé par {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Event(bot))
