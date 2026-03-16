import discord
from discord.ext import tasks
from datetime import datetime
from zoneinfo import ZoneInfo
import os

TOKEN = os.getenv("TOKEN")

CHANNEL_ID = 1451901256430915604

intents = discord.Intents.default()
client = discord.Client(intents=intents)

MSK = ZoneInfo("Europe/Moscow")

SCHEDULE = {
    ("Everyday", "21:30"): [
        "@everyone\n\n⏰ Guild Party начнётся через 30 минут!\n🕒 Сегодня в 22:00 МСК"
    ],
    ("Everyday", "22:00"): [
        "@everyone\n\n🔥 Guild Party началось!\n🕒 Сегодня в 22:00 МСК"
    ],

    ("Monday", "21:00"): [
        "@everyone\n\n⏰ Test Your Skills начнётся через 30 минут!\n🕒 Сегодня в 21:30 МСК"
    ],
    ("Monday", "21:30"): [
        "@everyone\n\n⚔️ Test Your Skills началось!\n🕒 Сегодня в 21:30 МСК"
    ],

    ("Tuesday", "21:00"): [
        "@everyone\n\n⏰ Test Your Skills начнётся через 30 минут!\n🕒 Сегодня в 21:30 МСК"
    ],
    ("Tuesday", "21:30"): [
        "@everyone\n\n⚔️ Test Your Skills началось!\n🕒 Сегодня в 21:30 МСК"
    ],

    ("Wednesday", "20:30"): [
        "@everyone\n\n⏰ Breaking Army начнётся через 30 минут!\n🕒 Сегодня в 21:00–23:00 МСК"
    ],
    ("Wednesday", "21:00"): [
        "@everyone\n\n🛡️ Breaking Army началось!\n🕒 Сегодня в 21:00–23:00 МСК"
    ],

    ("Friday", "20:30"): [
        "@everyone\n\n⏰ Breaking Army начнётся через 30 минут!\n🕒 Сегодня в 21:00–23:00 МСК"
    ],
    ("Friday", "21:00"): [
        "@everyone\n\n🛡️ Breaking Army началось!\n🕒 Сегодня в 21:00–23:00 МСК"
    ],
}

sent_today = set()
last_date = None


@client.event
async def on_ready():
    print(f"Бот запущен как {client.user}")

    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("✅ Бот работает и подключился!")

    if not reminder_loop.is_running():
        reminder_loop.start()


@tasks.loop(seconds=20)
async def reminder_loop():
    global sent_today, last_date

    now = datetime.now(MSK)
    today = now.date()
    weekday = now.strftime("%A")
    current_time = now.strftime("%H:%M")

    if last_date != today:
        sent_today = set()
        last_date = today

    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        return

    keys_to_check = [
        ("Everyday", current_time),
        (weekday, current_time),
    ]

    for key in keys_to_check:
        if key in SCHEDULE and key not in sent_today:
            messages = SCHEDULE[key]

            for message in messages:
                await channel.send(
                    message,
                    allowed_mentions=discord.AllowedMentions(everyone=True)
                )

            sent_today.add(key)


@reminder_loop.before_loop
async def before_loop():
    await client.wait_until_ready()


client.run(TOKEN)
