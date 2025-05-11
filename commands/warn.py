import discord
from discord.ext import commands
from discord import app_commands
import json
import os


class Warn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = "warns.json"
        self.warnings = self.load_warnings()

    def load_warnings(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_warnings(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.warnings, f, indent=4)

    @app_commands.command(name="warn", description="Avertit un membre avec une raison")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        if str(member.id) == str(interaction.user.id):
            await interaction.response.send_message("❌ Tu ne peux pas t'avertir toi-même.", ephemeral=True)
            return
        if member.id == self.bot.user.id:
            await interaction.response.send_message("❌ Tu ne peux pas avertir le bot.", ephemeral=True)
            return

        self.warnings.setdefault(str(member.id), []).append({
            "mod": interaction.user.name,
            "reason": reason
        })
        self.save_warnings()

        embed = discord.Embed(
            title="⚠️ Avertissement",
            description=f"{member.mention} a été averti.",
            color=discord.Color.yellow()
        )
        embed.add_field(name="Raison", value=reason, inline=False)
        embed.set_footer(text=f"Averti par {interaction.user}")

        await interaction.response.send_message(embed=embed)

        try:
            await member.send(f"⚠️ Tu as été averti sur **{interaction.guild.name}** pour : **{reason}**")
        except discord.Forbidden:
            pass


async def setup(bot):
    await bot.add_cog(Warn(bot))
