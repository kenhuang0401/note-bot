import os
from discord.ext import commands
from dotenv import load_dotenv
from supabase import create_client, Client
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run():
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )

Thread(
    target=run,
    daemon=True
).start()

# 載入 .env 檔案
load_dotenv()

# 取得 Bot Token
TOKEN = os.getenv("DISCORD_TOKEN")
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise RuntimeError("✗ SUPABASE_URL or SUPABASE_KEY not found in .env")
supabase: Client = create_client(url, key)

# 設定 intents（機器人能接收的事件類型）
try:
    from discord import Intents
    intents = Intents.default()
    intents.message_content = True
except Exception:
    intents = None

# 初始化 Bot
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    """Bot 連接成功時觸發"""
    print(f"✓ 機器人 {bot.user} 登入成功")


@bot.event
async def setup_hook():
    await bot.load_extension("cogs.slides")
    await bot.load_extension("cogs.add")
    await bot.load_extension("cogs.delete")
    await bot.tree.sync()

bot.setup_hook = setup_hook


if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("✗ DISCORD_TOKEN not found in .env")
    bot.run(TOKEN)
