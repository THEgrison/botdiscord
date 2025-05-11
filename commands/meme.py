import discord
from discord.ext import commands
from discord import app_commands
import aiohttp


class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="meme", description="Envoie un mème aléatoire depuis Reddit")
    async def meme(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://meme-api.com/gimme") as response:
                if response.status == 200:
                    data = await response.json()
                    embed = discord.Embed(title=data["title"], url=data["postLink"], color=discord.Color.random())
                    embed.set_image(url=data["url"])
                    embed.set_footer(text=f"👍 {data['ups']} | r/{data['subreddit']} | par u/{data['author']}")
                    await interaction.response.send_message(embed=embed)
                else:
                    await interaction.response.send_message("❌ Impossible de récupérer un mème pour le moment.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Meme(bot))
