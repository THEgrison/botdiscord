import discord
from discord.ext import commands
from discord import app_commands


class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="avatar", description="Affiche l'avatar d'un membre")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user

        embed = discord.Embed(
            title=f"🖼️ Avatar de {member}",
            color=discord.Color.blue()
        )

        embed.set_image(url=member.display_avatar.url)
        embed.set_footer(text=f"Demandé par {interaction.user}", icon_url=interaction.user.display_avatar.url)

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Avatar(bot))
