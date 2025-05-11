import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import asyncio

# --- Serveur Flask pour UptimeRobot ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Je suis vivant !"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_flask).start()

# --- Discord Bot ---
TOKEN = os.environ['TOKEN']
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    await bot.tree.sync()
    print("📜 Commandes chargées :", [cmd.name for cmd in bot.tree.get_commands()])

async def load_extensions():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"commands.{filename[:-3]}")
                print(f"✅ {filename} chargé avec succès")
            except Exception as e:
                print(f"❌ Erreur lors du chargement de {filename}: {e}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

await bot.load_extension("commands.warn")
await bot.load_extension("commands.clearwarns")
await bot.load_extension("commands.warnings")

asyncio.run(main())
