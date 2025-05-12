import discord
from discord.ext import commands
from discord import app_commands

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="invite", description="https://discord.com/oauth2/authorize?client_id=1099734590756761761&permissions=8&integration_type=0&scope=bot")
    async def invite(self, interaction: discord.Interaction):
        invite_url = discord.utils.oauth_url(self.bot.user.id, permissions=discord.Permissions.all())
        await interaction.response.send_message(f"Invite-moi avec ce lien : {invite_url}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Invite(bot))
