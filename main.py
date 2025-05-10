import os
import discord
from discord.ext import commands

TOKEN = os.environ['TOKEN']
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    await bot.tree.sync()
    print("📜 Commandes chargées :",
          [command.name for command in bot.tree.get_commands()])

async def load_extensions():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            try:
                cog_name = f"commands.{filename[:-3]}"
                await bot.load_extension(cog_name)
                print(f"✅ {filename} chargé avec succès")
            except Exception as e:
                print(f"❌ Erreur lors du chargement de {filename}: {e}")

import asyncio

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

asyncio.run(main())
