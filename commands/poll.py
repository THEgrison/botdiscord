import discord
from discord.ext import commands
from discord import app_commands


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="poll", description="Crée un sondage à deux options")
    async def poll(self, interaction: discord.Interaction, question: str, option1: str, option2: str):
        embed = discord.Embed(title="📊 Sondage", description=question, color=discord.Color.purple())
        embed.add_field(name="1️⃣", value=option1, inline=False)
        embed.add_field(name="2️⃣", value=option2, inline=False)
        poll_message = await interaction.channel.send(embed=embed)
        await poll_message.add_reaction("1️⃣")
        await poll_message.add_reaction("2️⃣")
        await interaction.response.send_message("✅ Sondage créé !", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Poll(bot))
