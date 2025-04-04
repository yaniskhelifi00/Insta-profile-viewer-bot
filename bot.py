from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from bs4 import BeautifulSoup

# Scraping function
def get_instagram_stats(username):
    url = f"https://www.instagram.com/{username}/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        return None

    soup = BeautifulSoup(r.text, 'html.parser')
    meta = soup.find("meta", property="og:description")

    if not meta:
        return None

    content = meta["content"]
    # Example: '1,234 Followers, 56 Following, 123 Posts - See Instagram photos and videos from ...'
    parts = content.split(", ")
    followers = parts[0].split(" ")[0]
    following = parts[1].split(" ")[0]

    return followers, following

# Telegram command handler
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Utilisation : /stats <nom_utilisateur>")
        return

    username = context.args[0]
    stats = get_instagram_stats(username)

    if stats:
        followers, following = stats
        await update.message.reply_text(f"**@{username}**\nFollowers: {followers}\nFollowing: {following}")
    else:
        await update.message.reply_text("Impossible de récupérer les données. Le profil est peut-être privé ou inexistant.")

# Run the bot
async def main():
    app = ApplicationBuilder().token("YOUR_TELEGRAM_BOT_TOKEN").build()
    app.add_handler(CommandHandler("stats", stats))
    print("Bot running...")
    await app.run_polling()