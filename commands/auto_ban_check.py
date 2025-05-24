import discord
from discord.ext import commands

class AutoBanCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1275015770816118784  # Ton salon de logs

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if "boa" in member.name.lower():
            channel = self.bot.get_channel(self.channel_id)
            if not channel:
                return

            embed = discord.Embed(
                title="🛑 Détection automatique",
                description=f"Le membre {member.mention} (`{member.name}`) contient 'boa' dans son nom.",
                color=discord.Color.orange()
            )
            embed.set_footer(text="Souhaitez-vous le bannir ?")

            view = BanConfirmationView(member)
            await channel.send(embed=embed, view=view)

class BanConfirmationView(discord.ui.View):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=60)
        self.member = member

    @discord.ui.button(label="✅ Bannir", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await self.member.ban(reason="Nom contient 'boa'. Bannissement confirmé.")
            await interaction.response.send_message(f"{self.member} a été **banni**.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Erreur : {e}", ephemeral=True)
        self.stop()

    @discord.ui.button(label="❌ Ignorer", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"Action ignorée. {self.member} n'a pas été banni.", ephemeral=True)
        self.stop()

async def setup(bot):
    await bot.add_cog(AutoBanCheck(bot))
