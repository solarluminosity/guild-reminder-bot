import os
import discord
from discord.ext import tasks
from datetime import datetime
from zoneinfo import ZoneInfo

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1451901256430915604

intents = discord.Intents.default()
client = discord.Client(intents=intents)

MSK = ZoneInfo("Europe/Moscow")

SCHEDULE = {
    ("Monday", "21:30"): [
        "⚔️ Test Your Skills началось!",
        "⏰ Guild Party через 30 минут!"
    ],
    ("Tuesday", "21:30"): [
        "⚔️ Test Your Skills началось!",
        "⏰ Guild Party через 30 минут!"
    ],
    ("Wednesday", "21:00"): [
        "🛡️ Breaking Army началось! (21:00–23:00)"
    ],
    ("Friday", "21:00"): [
        "🛡️ Breaking Army началось! (21:00–23:00)"
    ],

    ("Everyday", "21:55"): [
        "⚠️ Guild Party через 5 минут!"
    ],
    ("Everyday", "22:00"): [
        "🔥 Guild Party началось!"
    ],
}

sent_today = set()
last_date = None


@client.event
async def on_ready():
    print(f"Бот запущен как {client.user}")
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
        print("Не удалось найти канал. Проверь CHANNEL_ID.")
        return

    keys_to_check = [
        ("Everyday", current_time),
        (weekday, current_time),
    ]

    for key in keys_to_check:
        if key in SCHEDULE and key not in sent_today:
            messages = SCHEDULE[key]
            for message in messages:
                await channel.send(message)
            sent_today.add(key)


@reminder_loop.before_loop
async def before_loop():
    await client.wait_until_ready()


if TOKEN is None:
    raise ValueError("TOKEN не найден. Добавь его в переменные среды.")

client.run(TOKEN)