import discord
from discord.ext import commands
import asyncio

class RestoreMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1370525322231021588  # ID du salon à surveiller
        self.author_id = 714114719014715412   # TON ID à toi (pour ignorer si c’est toi)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.channel.id != self.channel_id:
            return
        if message.author.id != self.bot.user.id:
            return  # On ne restaure que les messages du bot

        await asyncio.sleep(1)  # Attendre pour que l'audit log soit dispo

        try:
            async for entry in message.guild.audit_logs(
                limit=5,
                action=discord.AuditLogAction.message_delete
            ):
                if entry.target.id == self.bot.user.id and abs((discord.utils.utcnow() - entry.created_at).total_seconds()) < 5:
                    if entry.user.id != self.author_id:
                        await message.channel.send(
                            f"🔁 **Message du bot restauré après suppression par {entry.user.mention}** :\n> {message.content}"
                        )
                    else:
                        print("🛑 Tu as supprimé le message, donc il n’est pas restauré.")
                    return
        except discord.Forbidden:
            print("❌ Le bot n’a pas la permission de voir les logs d’audit.")
        except Exception as e:
            print(f"❌ Erreur lors de la récupération du log : {e}")

async def setup(bot):
    await bot.add_cog(RestoreMessage(bot))
