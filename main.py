import os
import discord
from discord.ext import commands, tasks
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask
from threading import Thread
from discord import FFmpegPCMAudio
import pytz
import asyncio

load_dotenv()
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
VOICE_CHANNEL_ID = int(os.getenv("VOICE_CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

tz = pytz.timezone("Asia/Bangkok")

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

weekly_schedule = {
    "daily": {
        "00:50": {"msg": "🛌💤 ดึกแค่ไหนก็ต้องพร้อม! เตรียมตัวลง วัลฮัลลา กันน้าาา 🌌 @everyone", "mp3": "ho.mp3"},
        "02:50": {"msg": "หลับกันยังเอ่ย ! 💢 ไปอัด บอสกราม 💀 แล้วต่อ บอสบัลเดอร์ ⚔️ @everyone", "mp3": "yo.mp3"},
        "03:50": {"msg": "💤 ถ้ายังไหว เตรียมตัวลง วัลฮัลลา กันน้าาา 💀🔮 @everyone", "mp3": "ho.mp3"},
        "18:50": {"msg": "🚨พับเพียบรวมตัว 💥 ไปอัด บอสกราม 💀 ต่อด้วยซัด บอสบัลเดอร์ ⚔️ @everyone", "mp3": "yo.mp3"},
        "19:50": {"msg": "⚔️ เตรียมตัวลง วัลฮัลลา กันน้าาา 🛡️✨ @everyone", "mp3": "ho.mp3"},
    },
    6: {
        "12:00": {"msg": "⏰ แจ้งเตือนกันลืม! วันนี้มี ดันกิลด์ ตอนสามทุ่มนะคับผม 🏰🔥 @everyone", "mp3": "yo.mp3"},
        "18:50": {"msg": "🚨พับเพียบรวมตัว 💥 ไปอัด บอสกราม 💀 ต่อด้วยซัด บอสบัลเดอร์ ⚔️ @everyone", "mp3": "yo.mp3"},
        "19:50": {"msg": "⚔️ เตรียมตัวลง วัลฮัลลา กันน้าาา 🛡️✨ @everyone", "mp3": "ho.mp3"},
        "20:30": {"msg": "📣 อีก 30 นาที จะลง ดันกิลด์ แล้ววว! เตรียมตัวให้พร้อมนะคะ 💪 @everyone", "mp3": "yo.mp3"},
        "20:55": {"msg": "🚨 ใครยังไม่เข้าห้องเสียง มาด่วน!! 🎧 ดันกิลด์ จะเริ่มแล้วค่ะ ⚔️👑 @everyone", "mp3": "ho.mp3"},
        "00:50": {"msg": "🛌💤 ดึกแค่ไหนก็ต้องพร้อม! เตรียมตัวลง วัลฮัลลา กันน้าาา 🌌 @everyone", "mp3": "ho.mp3"},
        "02:50": {"msg": "หลับกันยังเอ่ย ! 💢 ไปอัด บอสกราม 💀 แล้วต่อ บอสบัลเดอร์ ⚔️ @everyone", "mp3": "yo.mp3"},
        "03:50": {"msg": "💤 ถ้ายังไหว เตรียมตัวลง วัลฮัลลา กันน้าาา 💀🔮 @everyone", "mp3": "ho.mp3"},
    }
}

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    send_message.start()

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
        voice_channel = bot.get_channel(VOICE_CHANNEL_ID)

        for entry in messages:
            if channel:
                await channel.send(entry["msg"])
            if isinstance(voice_channel, discord.VoiceChannel):
                vc = await voice_channel.connect()
                audio = FFmpegPCMAudio(entry["mp3"])
                vc.play(audio)
                while vc.is_playing():
                    await asyncio.sleep(1)
                await vc.disconnect()

keep_alive()
bot.run(TOKEN)
