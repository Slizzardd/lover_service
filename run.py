import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from fastapi import FastAPI, Request

TOKEN = "8730984401:AAGohTP7eBoOUpnQhRFoh4pYk-3i6eQyapo"
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"https://your-app.onrender.com{WEBHOOK_PATH}"

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