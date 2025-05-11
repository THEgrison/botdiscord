import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class Warns(commands.Cog):
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

    warn_group = app_commands.Group(name="warn", description="Gérer les avertissements")

    @warn_group.command(name="add", description="Avertit un membre avec une raison")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def add(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        if member.id == interaction.user.id:
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

    @warn_group.command(name="list", description="Affiche les avertissements d’un membre")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def list(self, interaction: discord.Interaction, member: discord.Member):
        warns = self.warnings.get(str(member.id))
        if not warns:
            await interaction.response.send_message(f"✅ {member.mention} n'a aucun avertissement.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"📋 Avertissements de {member}",
            color=discord.Color.orange()
        )

        for i, warn in enumerate(warns, start=1):
            embed.add_field(
                name=f"⚠️ Avertissement {i}",
                value=f"**Modérateur :** {warn['mod']}\n**Raison :** {warn['reason']}",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

    @warn_group.command(name="clear", description="Supprime tous les avertissements d’un membre")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, member: discord.Member):
        if str(member.id) not in self.warnings or not self.warnings[str(member.id)]:
            await interaction.response.send_message(f"{member.mention} n’a aucun avertissement à supprimer.", ephemeral=True)
            return

        del self.warnings[str(member.id)]
        self.save_warnings()

        await interaction.response.send_message(f"✅ Tous les avertissements de {member.mention} ont été supprimés.")

    async def cog_load(self):
        self.bot.tree.add_command(self.warn_group)

async def setup(bot):
    await bot.add_cog(Warns(bot))
