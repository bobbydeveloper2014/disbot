import discord
from discord.ext import commands
from openai import OpenAI

# ====== NHÉT KEY VÀO ĐÂY ======
DISCORD_TOKEN = "MTQ0NjAwNDM1NjE2NzIzNzY2NA.GfE5vP.U3oIbpZ0c-waQSHni0PBwPBtu5Cqo_DzsGxUCQ"
OPENAI_KEY = "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"
# ==============================

client_ai = OpenAI(api_key=OPENAI_KEY)

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

    # trigger: bot được tag hoặc dùng !ask
    if bot.user.mentioned_in(message) or message.content.startswith("!ask"):
        user_text = (
            message.content.replace(f"<@{bot.user.id}>", "")
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
                    {"role": "system", "content": "Bạn là bot Discord trả lời ngắn, rõ ràng."},
                    {"role": "user", "content": user_text}
                ]
            )

            reply_text = response.choices[0].message.content
            await message.reply(reply_text)

        except Exception as e:
            await message.reply("Lỗi khi gọi API: " + str(e))

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
