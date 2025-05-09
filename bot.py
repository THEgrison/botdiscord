import discord
import os
import asyncio
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# Charger le token depuis un fichier .env
load_dotenv("token.env")  
TOKEN = os.getenv("DISCORD_TOKEN")

# Définir les intents nécessaires
intents = discord.Intents.default()
intents.message_content = True  

# Initialiser le bot
bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)  # Désactiver le help par défaut

# Vérification globale : Seuls les administrateurs peuvent exécuter les commandes
@bot.check
async def globally_admin_only(ctx):
    return ctx.author.guild_permissions.administrator  # Vérifie si l'utilisateur est admin

# Quand le bot est prêt
@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    
    # Synchronisation des commandes slash avec Discord
    await bot.tree.sync()
    print("📜 Commandes chargées :", [command.name for command in bot.tree.get_commands()])

# Charger automatiquement les fichiers de cogs
async def load_extensions():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            try:
                cog_name = f"commands.{filename[:-3]}"  
                await bot.load_extension(cog_name)
                print(f"✅ {filename} chargé avec succès")
            except Exception as e:
                print(f"❌ Erreur lors du chargement de {filename}: {e}")

# Fonction principale pour charger les cogs et démarrer le bot
async def main():
    async with bot:
        await load_extensions()  # Charger tous les cogs
        await bot.start(TOKEN)  # Démarrer le bot

# Lancer le bot
asyncio.run(main())
