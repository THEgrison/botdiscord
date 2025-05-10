import os
import discord
from discord.ext import commands
from flask import Flask

# --- Serveur Flask pour UptimeRobot ---
app = Flask('')

# Route principale qui renvoie un message pour vérifier que le bot est vivant
@app.route('/')
def home():
    return "Je suis vivant !"  # Message envoyé pour la vérification d'UptimeRobot

# --- Discord Bot ---

# Charger le token depuis les variables d'environnement
TOKEN = os.environ['TOKEN']

# Définir les intents nécessaires
intents = discord.Intents.default()
intents.message_content = True

# Initialiser le bot
bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)

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

# Fonction principale pour démarrer le bot
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

# Lancer le bot
import asyncio
asyncio.run(main())

# Lancer Flask dans un thread séparé
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Railway définit cette variable automatiquement
    app.run(host='0.0.0.0', port=port)  # Flask lancé avec `app.run()` pour le développement
