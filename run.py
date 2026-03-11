import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from fastapi import FastAPI, Request

TOKEN = "BOT_TOKEN"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = "https://your-app.onrender.com/webhook"

bot = Bot(token=TOKEN)
dp = Dispatcher()

app = FastAPI()


# Команда /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Бот работает через webhook 🚀")


# endpoint для Telegram
@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    update = await request.json()
    await dp.feed_raw_update(bot, update)
    return {"ok": True}


# запуск
@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()