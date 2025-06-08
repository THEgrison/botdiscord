import discord
from discord.ext import commands

class RestoreMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1370525322231021588  # ID du salon ciblé
        self.author_id = 714114719014715412    # TON ID utilisateur

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        # On vérifie si le message est dans le bon salon et vient du bot lui-même
        if (
            message.channel.id == self.channel_id and
            message.author.id == self.bot.user.id and
            message.content
        ):
            # On récupère les derniers audit logs pour voir qui a supprimé
            async for entry in message.guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
                if entry.target.id == self.bot.user.id and entry.user.id != self.author_id:
                    # Si ce n'est PAS toi qui l’as supprimé, on le restaure
                    repost = (
                        f"🔁 **Message du bot restauré** :\n"
                        f"> {message.content}"
                    )
                    await message.channel.send(repost)
                    break  # on sort dès qu'on a trouvé le bon log

async def setup(bot):
    await bot.add_cog(RestoreMessage(bot))
