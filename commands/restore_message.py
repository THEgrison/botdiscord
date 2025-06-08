import discord
from discord.ext import commands

class RestoreMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1106114283231776790  # Remplace par l'ID de ton salon
        self.author_id = 714114719014715412  # Remplace par TON ID utilisateur

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        # Vérifie que le message supprimé correspond bien aux critères
        if (
            message.channel.id == self.channel_id and
            message.author.id == self.author_id and
            not message.author.bot and
            message.content
        ):
            # Reposte le message
            repost = (
                f"🔁 **Message restauré de {message.author.mention}** :\n"
                f"> {message.content}"
            )
            await message.channel.send(repost)

async def setup(bot):
    await bot.add_cog(RestoreMessage(bot))
