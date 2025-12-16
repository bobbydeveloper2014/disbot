import discord
from discord.ext import commands

from openai import OpenAI
from dotenv import load_dotenv
import os

from flask import Flask
from threading import Thread

# =====================
# Load biến môi trường
# =====================
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

# =====================
# OpenAI client
# =====================
client_ai = OpenAI(api_key=OPENAI_KEY)

# =====================
# Flask app (chạy ngầm)
# =====================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive", 200

def run_flask():
    # 0.0.0.0 để deploy / keep-alive
    app.run(host="0.0.0.0", port=3000)

# =====================
# Discord bot
# =====================
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot đã online dưới tên: {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message) or message.content.startswith("!ask"):
        user_text = (
            message.content
            .replace(f"<@{bot.user.id}>", "")
            .replace("!ask", "")
            .strip()
        )

        if not user_text:
            await message.reply("Bạn muốn hỏi gì?")
            return

        try:
            response = client_ai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Bạn là bot Discord, trả lời ngắn gọn, rõ ràng."
                    },
                    {
                        "role": "user",
                        "content": user_text
                    }
                ]
            )

            reply_text = response.choices[0].message.content
            await message.reply(reply_text)

        except Exception as e:
            await message.reply("Lỗi khi gọi API: " + str(e))

    await bot.process_commands(message)

# =====================
# Main
# =====================
if __name__ == "__main__":
    # Chạy Flask ở thread riêng
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Chạy Discord bot
    bot.run(DISCORD_TOKEN)
