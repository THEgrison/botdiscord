import discord
from discord.ext import commands
import asyncio

class RestoreMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1370525322231021588  # Salon à surveiller
        self.author_id = 714114719014715412    # Ton ID

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.channel.id != self.channel_id:
            return
        if message.author.bot and message.author.id != self.bot.user.id:
            return  # Ignore les autres bots

        await asyncio.sleep(1)  # Attendre un peu pour que l’audit log soit à jour

        # Vérifie qui a supprimé
        deleter = None
        try:
            async for entry in message.guild.audit_logs(limit=5, action=discord.AuditLogAction.message_delete):
                if (
                    entry.target.id == message.author.id
                    and abs((discord.utils.utcnow() - entry.created_at).total_seconds()) < 5
                    and entry.extra.channel.id == message.channel.id
                ):
                    deleter = entry.user
                    break
        except discord.Forbidden:
            print("❌ Pas accès aux logs d'audit.")
        except Exception as e:
            print(f"⚠️ Erreur audit logs : {e}")

        # Cas 1 : Ton message (author_id) est supprimé → on restaure
        if message.author.id == self.author_id and message.content:
            await message.channel.send(
                f"🔁 **Message restauré de {message.author.mention}** :\n> {message.content}"
            )
            return

        # Cas 2 : Message du bot est supprimé par quelqu’un d’autre que toi → on restaure
        if (
            message.author.id == self.bot.user.id
            and message.content
            and deleter is not None
            and deleter.id != self.author_id
        ):
            await message.channel.send(
                f"🔁 **Message du bot restauré après suppression par {deleter.mention}** :\n> {message.content}"
            )

async def setup(bot):
    await bot.add_cog(RestoreMessage(bot))
