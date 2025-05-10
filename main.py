import discord
import os
import asyncio
from discord.ext import commands
from discord import app_commands
from flask import Flask
from threading import Thread

# --- Serveur Flask pour UptimeRobot ---
app = Flask('')

# Route principale qui renvoie un message pour vérifier que le bot est vivant
@app.route('/')
def home():
    return "Je suis vivant !"  # Message envoyé pour la vérification d'UptimeRobot

# Fonction pour démarrer le serveur Flask avec Gunicorn
def run():
    port = int(os.environ.get("PORT", 8080))  # Railway définit cette variable automatiquement
    # Gunicorn prendra en charge le lancement du serveur

# Lancer Flask dans un thread pour ne pas bloquer l'exécution du bot Discord
Thread(target=run).start()

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


# Fonction principale
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


# Lancer le bot
asyncio.run(main())
