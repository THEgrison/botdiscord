import discord
import os
import asyncio
from discord.ext import commands
from discord import app_commands
from flask import Flask
from threading import Thread

# --- Discord Bot ---

# Charger le token depuis les variables d'environnement (Replit Secrets)
TOKEN = os.environ['TOKEN']

# Définir les intents nécessaires
intents = discord.Intents.default()
intents.message_content = True

# Initialiser le bot
bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)

# Vérification globale : Seuls les administrateurs peuvent exécuter les commandes
@bot.check
async def globally_admin_only(ctx):
    return ctx.author.guild_permissions.administrator

# Quand le bot est prêt
@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    await bot.tree.sync()
    print("📜 Commandes chargées :",
          [command.name for command in bot.tree.get_commands()])

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

# Fonction Flask pour empêcher l'instance Railway de dormir
app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running!', 200

# Fonction principale pour lancer le bot et Flask
async def main():
    # Lancer le bot Discord
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

# Lancer le bot dans un thread séparé pour éviter de bloquer le processus Flask
def run_bot():
    asyncio.run(main())

# Lancez le bot dans un thread afin de ne pas bloquer le serveur Flask
if __name__ == "__main__":
    # Démarrer le thread pour le bot
    thread = Thread(target=run_bot)
    thread.daemon = True  # S'assure que le thread termine lorsque l'application se ferme
    thread.start()

    # Lancer Flask avec Gunicorn
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
