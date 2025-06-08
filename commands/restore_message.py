import discord
from discord.ext import commands

class RestoreMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1106114283231776790  # Salon à surveiller
        self.author_id = 714114719014715412    # Ton ID

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.channel.id != self.channel_id:
            return
        if not message.content:
            return  # Ignore les messages sans texte

        # Cas 1 : ton message est supprimé → on restaure
        if message.author.id == self.author_id:
            await message.channel.send(
                f"🔁 **Message restauré de {message.author.mention}** :\n> {message.content}"
            )
            return

        # Cas 2 : un message du bot est supprimé → on restaure
        if message.author.id == self.bot.user.id:
            await message.channel.send(
                f"🔁 **Message du bot restauré** :\n> {message.content}"
            )

async def setup(bot):
    await bot.add_cog(RestoreMessage(bot))
