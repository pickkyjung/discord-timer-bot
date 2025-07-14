import os
import discord
from discord.ext import commands, tasks
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask
from threading import Thread
import pytz

# โหลด TOKEN / ID จาก .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# ใช้ intents แบบมี message content (สำคัญมาก)
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
tz = pytz.timezone("Asia/Bangkok")

# == Flask สำหรับ uptime robot ==
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# == ตารางเวลาส่งข้อความ ==
weekly_schedule = {
    "daily": {
        "18:50": "🚨พับเพียบรวมตัว 💥 ไปอัด บอสกราม 💀 ต่อด้วยซัด บอสบัลเดอร์ ⚔️ @everyone",
        "19:50": "⚔️ เตรียมตัวลง วัลฮัลลา กันน้าาา 🛡️✨ @everyone",
    },
    6: {
        "12:00": "⏰ แจ้งเตือนกันลืม! วันนี้มี ดันกิลด์ ตอนสามทุ่มนะคับผม 🏰🔥 @everyone",
        "20:30": "📣 อีก 30 นาที จะลง ดันกิลด์ แล้ววว! เตรียมตัวให้พร้อมนะคะ 💪 @everyone",
        "20:55": "🚨 ใครยังไม่เข้าห้องเสียง มาด่วน!! 🎧 ดันกิลด์ จะเริ่มแล้วค่ะ ⚔️👑 @everyone",
    }
}

# == บอทพร้อม ==
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    send_message.start()

# == สั่ง !test ได้ ==
@bot.command()
async def test(ctx):
    print(f"📩 รับคำสั่ง !test จาก {ctx.author}")
    await ctx.send("บอทยังทำงานอยู่นะครับ!")

# == ส่งข้อความตามเวลา ==
@tasks.loop(seconds=60)
async def send_message():
    now = datetime.now(tz)
    time_now = now.strftime('%H:%M')
    weekday = now.weekday()

    messages = []

    if time_now in weekly_schedule["daily"]:
        messages.append(weekly_schedule["daily"][time_now])

    if weekday in weekly_schedule and time_now in weekly_schedule[weekday]:
        messages.append(weekly_schedule[weekday][time_now])

    if messages:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            for msg in messages:
                await channel.send(msg)

# == เริ่ม Flask + บอท ==
keep_alive()
bot.run(TOKEN)
