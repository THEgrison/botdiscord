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

        self.warn_group = app_commands.Group(name="warn", description="Gérer les avertissements")
        self.warn_group.command(name="add", description="Avertit un membre avec une raison")(self.add)
        self.warn_group.command(name="list", description="Affiche les avertissements d’un membre")(self.list)
        self.warn_group.command(name="clear", description="Supprime tous les avertissements d’un membre")(self.clear)

    def load_warnings(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_warnings(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.warnings, f, indent=4)

    # --- /warn add ---
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

    # --- /warn list ---
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

        view = DeleteWarningView(self, member.id, warns, interaction.user)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    # --- /warn clear ---
    async def clear(self, interaction: discord.Interaction, member: discord.Member):
        if str(member.id) not in self.warnings or not self.warnings[str(member.id)]:
            await interaction.response.send_message(f"{member.mention} n’a aucun avertissement à supprimer.", ephemeral=True)
            return

        del self.warnings[str(member.id)]
        self.save_warnings()

        await interaction.response.send_message(f"✅ Tous les avertissements de {member.mention} ont été supprimés.")

    async def cog_load(self):
        self.bot.tree.add_command(self.warn_group)


class DeleteWarningView(discord.ui.View):
    def __init__(self, cog: Warns, user_id: int, warnings: list, moderator: discord.User):
        super().__init__(timeout=60)
        self.cog = cog
        self.user_id = user_id
        self.moderator = moderator

        for i in range(len(warnings)):
            self.add_item(DeleteButton(i + 1, self))


class DeleteButton(discord.ui.Button):
    def __init__(self, index: int, view: DeleteWarningView):
        super().__init__(label=f"Supprimer ⚠️{index}", style=discord.ButtonStyle.danger, custom_id=str(index))
        self.index = index - 1
        self.view_obj = view

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.view_obj.moderator.id:
            await interaction.response.send_message("❌ Seul l'auteur de la commande peut supprimer un avertissement.", ephemeral=True)
            return

        user_id_str = str(self.view_obj.user_id)
        try:
            del self.view_obj.cog.warnings[user_id_str][self.index]
            if not self.view_obj.cog.warnings[user_id_str]:
                del self.view_obj.cog.warnings[user_id_str]
            self.view_obj.cog.save_warnings()
            await interaction.response.send_message(f"✅ Avertissement n°{self.index + 1} supprimé.", ephemeral=True)
        except IndexError:
            await interaction.response.send_message("❌ Cet avertissement n'existe plus.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Warns(bot))
