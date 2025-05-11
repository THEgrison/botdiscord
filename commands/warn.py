import discord
from discord.ext import commands
from discord import app_commands
from collections import defaultdict


class Warn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = defaultdict(list)  # Dictionnaire {user_id: [liste des avertissements]}

    @app_commands.command(name="warn", description="Avertit un membre avec une raison")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        # Empêche d'avertir soi-même ou le bot
        if member.id == interaction.user.id:
            await interaction.response.send_message("❌ Tu ne peux pas t'avertir toi-même.", ephemeral=True)
            return
        if member.id == self.bot.user.id:
            await interaction.response.send_message("❌ Tu ne peux pas avertir le bot.", ephemeral=True)
            return

        self.warnings[member.id].append({
            "mod": interaction.user.name,
            "reason": reason
        })

        embed = discord.Embed(
            title="⚠️ Avertissement",
            description=f"{member.mention} a été averti.",
            color=discord.Color.yellow()
        )
        embed.add_field(name="Raison", value=reason, inline=False)
        embed.set_footer(text=f"Averti par {interaction.user}")

        await interaction.response.send_message(embed=embed)

        # Message privé au membre
        try:
            await member.send(f"⚠️ Tu as été averti sur **{interaction.guild.name}** pour : **{reason}**")
        except discord.Forbidden:
            pass  # DM fermés


async def setup(bot):
    await bot.add_cog(Warn(bot))
